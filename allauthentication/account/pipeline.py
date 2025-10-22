def save_profile(backend, user, response, *args, **kwargs):
    """
    Extract full name from social auth provider and activate the user
    """
    if backend.name == 'google-oauth2':
        # Get name from Google profile
        full_name = response.get('name', '')
        
        if full_name and (not user.full_name or user.full_name == user.email.split('@')[0]):
            user.full_name = full_name
        
        # Auto-activate OAuth users
        if not user.is_active:
            user.is_active = True
        
        user.save()
