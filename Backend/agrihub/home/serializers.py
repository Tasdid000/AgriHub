from rest_framework import serializers
from .models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str


from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "phone_Number", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before creating the user
        return User.objects.create_user(**validated_data)



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "image", "phone_Number", "address", "Farm_Name", "Farm_Type", "Farm_Size", "Farm_Location","is_admin", 'is_active']

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    Farm_Name = serializers.CharField(required=False)
    Farm_Type = serializers.PrimaryKeyRelatedField(queryset=Farm_Type.objects.all(), required=False)
    Farm_Size = serializers.CharField(required=False)
    Farm_Location = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("email", "name", "image", "phone_Number", "address", "Farm_Name", "Farm_Type", "Farm_Size", "Farm_Location")

    def validate_email(self, value):
        user = self.context['request'].user
        if value and User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You don't have permission for this user."})

        # Update fields based on the validated data
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_Number = validated_data.get('phone_Number', instance.phone_Number)
        instance.address = validated_data.get('address', instance.address)
        instance.Farm_Name = validated_data.get('Farm_Name', instance.Farm_Name)

        # Update the new fields if present
        instance.Farm_Type = validated_data.get('Farm_Type', instance.Farm_Type)
        instance.Farm_Size = validated_data.get('Farm_Size', instance.Farm_Size)
        instance.Farm_Location = validated_data.get('Farm_Location', instance.Farm_Location)

        instance.save()
        return instance
    
class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['current_password', 'password', 'password2']

    def validate(self, attrs):
        user = self.context.get('user')
        current_password = attrs.get('current_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Validate current password
        if not user.check_password(current_password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        # Validate new passwords
        if password != password2:
            raise serializers.ValidationError({"password": "New passwords must match."})

        return attrs

    def save(self):
        user = self.context.get('user')
        user.set_password(self.validated_data['password'])
        user.save()

# class SendPasswordResetEmailSerializer(serializers.Serializer):
#   email = serializers.EmailField(max_length=255)
#   class Meta:
#     fields = ['email']

#   def validate(self, attrs):
#     email = attrs.get('email')
#     if User.objects.filter(email=email).exists():
#       user = User.objects.get(email = email)
#       email = urlsafe_base64_encode(force_bytes(user.pk))
#       print('Encoded UID', email)
#       token = PasswordResetTokenGenerator().make_token(user)
#       print('Password Reset Token', token)      
#       link = f'http://localhost:3000/apiv1/user/reset/{email}/{token}'
#       print('Password Reset Link', link)
#       # Send EMail
#       body = 'Click Following Link to Reset Your Password '+link
#       data = {
#         'subject':'Reset Your Password',
#         'body':body,
#         'to_email':user.email
#       }
#       Util.send_email(data)
#       return attrs
#     else:
#       raise serializers.ValidationError('You are not a Registered User')


import logging

logger = logging.getLogger(__name__)

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')

        # Check if the user with the provided email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('You are not a Registered User')

        # Encode user ID and generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        logger.debug(f'Encoded UID: {uid}')
        logger.debug(f'Password Reset Token: {token}')

        # Construct the password reset link
        link = f'http://localhost:3000/apiv1/user/reset/{uid}/{token}'
        logger.debug(f'Password Reset Link: {link}')

        # Send email
        body = f'Click the following link to reset your password: {link}'
        data = {
            'subject': 'Reset Your Password',
            'body': body,
            'to_email': user.email
        }
        Util.send_email(data)

        return attrs

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      email = self.context.get('email')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      uid = force_str(urlsafe_base64_decode(email))
      user = User.objects.get(pk=uid)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class Contactserializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

#Farm_Type
class Farm_Typeserializers(serializers.ModelSerializer):
    class Meta:
        model = Farm_Type
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

class Appointment_time_slotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment_time_slot
        fields = "__all__"

class Video_conference_appointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video_conference_appointment
        fields = "__all__"

class Government_SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Government_Support
        fields = "__all__"


