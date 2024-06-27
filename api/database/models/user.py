from odmantic import Field, Model, ObjectId

class User(Model):
    """The user document format for the database"""

    object_id: ObjectId = Field(primary_field=True)
    id: str
    key: str
    banned: bool = Field(default=False)
    premium: bool = Field(default=False)
    
    model_config = {
        "collection": "users"
    }