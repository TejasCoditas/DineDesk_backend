from pydantic import BaseModel,model_validator

class Validation(BaseModel):


    # allow_empty: bool = False

    @model_validator(mode="before")
    @classmethod
    def strip_and_validate_strings(cls, data):
    
        if not isinstance(data, dict):
            return data
        
        allow_empty=data.pop("allow_empty",False)

        cleaned_data = {}
        for field, value in data.items():
            if isinstance(value, str):
                stripped = value.strip()

                    
                if not allow_empty and stripped=="":
                    raise ValueError(f"{field} cannot be empty or only whitespace")
                
                # if allow_empty and stripped=="":
                #     cleaned_data[field]=None
                #     continue

                cleaned_data[field] = stripped
            else:
                cleaned_data[field] = value

        # cleaned_data["allow_empty"] = allow_empty
        return cleaned_data
    