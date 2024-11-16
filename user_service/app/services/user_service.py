
async def get_user_from_db(db, user_id: int):
    query = "SELECT * FROM users WHERE id = $1"
    user = await db.fetchrow(query, user_id)
    
    if user:
        # Convert asyncpg.Record to a dictionary and handle datetime fields
        user_dict = dict(user)
        
        # Convert datetime fields (created_at and updated_at) to string if they are not None
        if user_dict['created_at']:
            user_dict['created_at'] = user_dict['created_at'].isoformat()
        if user_dict['updated_at']:
            user_dict['updated_at'] = user_dict['updated_at'].isoformat()
        
        return user_dict
    return None
async def get_username_from_db(db, user_id: str):
    query = "SELECT * FROM users WHERE username = $1"
    user = await db.fetchrow(query, user_id)
    
    if user:
        # Convert asyncpg.Record to a dictionary and handle datetime fields
        user_dict = dict(user)
        
        # Convert datetime fields (created_at and updated_at) to string if they are not None
        if user_dict['created_at']:
            user_dict['created_at'] = user_dict['created_at'].isoformat()
        if user_dict['updated_at']:
            user_dict['updated_at'] = user_dict['updated_at'].isoformat()
        
        return user_dict
    return None
async def create_user(db, name: str, username: str, password: str, role: str):
    
    query = """
        INSERT INTO users (name, username, password, role)
        VALUES ($1, $2, $3, $4)
        RETURNING name, username,password, role
    """
    # Execute the query and fetch the inserted record
    user = await db.fetchrow(query, name, username, password, role)
    
    if user:
        # Convert asyncpg.Record to a dictionary
        return dict(user)
    return None