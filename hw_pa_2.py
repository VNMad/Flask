from pydantic import (BaseModel, EmailStr, ValidationError, Field, field_validator)


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator('name')
    def validate_name(cls, value):
        if not value.replace(' ', '').isalpha():
            raise ValueError('The Name must contain only letters')
        return value

    @field_validator('age')
    def validate_age(cls, value):
        if value < 0 or value > 120:
            raise ValueError('Age must be between 0 and 120')
        return value

    @field_validator('is_employed')
    def validate_employment(cls, value, info):
        if not value: raise ValueError('User must be employed to register in this system')
        age = info.data.get('age')
        if age is not None:
            if age < 18 or age > 65:
                raise ValueError('Employed user must be between 18 and 65 years old')
        return value

def register_user(json_string):
    try:
        user = User.model_validate_json(json_string)
        print("User successfully registered:", user.name)
        print("\nSerialized JSON:")
        print(user.model_dump_json(indent=4))
        return user.model_dump_json

    except ValidationError as e:
        print("\nValidation error:", e)


if __name__ == "__main__":

    json_valid = """{
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    register_user(json_valid)

    print("\n" + "-" * 10 + "\n")
    json_invalid_age = """{
        "name": "Petr Kuznecov",
        "age": 70,
        "email": "petr.kuznecov@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    register_user(json_invalid_age)

    print("\n" + "-" * 10 + "\n")
    json_invalid_age = """{
        "name": "Petr Kuznecov",
        "age": 65,
        "email": "petr.kuznecov@example.com",
        "is_employed": false,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    register_user(json_invalid_age)


    print("\n" + "-" * 10 + "\n")
    json_invalid_email = """{
        "name": "Jack Russel",
        "age": 30,
        "email": "john.doe",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    register_user(json_invalid_email)

    print("\n" + "-" * 10 + "\n")
    json_invalid_name = """{
        "name": "John123",
        "age": 30,
        "email": "john@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    register_user(json_invalid_name)

    print("\n" + "-" * 10 + "\n")
    json_invalid_address = """{
        "name": "Ninja Turtle",
        "age": 30,
        "email": "john@example.com",
        "is_employed": true,
        "address": {
            "city": "N",
            "street": "St",
            "house_number": -10
        }
    }"""
    register_user(json_invalid_address)