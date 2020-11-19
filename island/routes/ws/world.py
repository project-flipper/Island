"""

CLIENT -> Authorization Header  [Verify, //Login//]
       -> event system
           -> Scopes
           -> Priority


scope => single string/Scope, list or tuple or iterable of string/Scope, or callable

@island_event.on(Event(type='PING', scopes=_or(['user:world:auth', 'user:world:init'])))
@has_scope()
@allow_once
@disable
async def handle_ping(ctx, *args, **kwargs):
    pass 

"""
