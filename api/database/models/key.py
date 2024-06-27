from odmantic import Field, Model, ObjectId

class Key(Model):
    """The provider key document format for the database"""

    object_id: ObjectId = Field(primary_field=True)
    name: str
    keys: list[str]
    
    model_config = {
        "collection": "keys"
    }