from graphene_gino import GinoConnectionField

class FilteredConnectionField(GinoConnectionField):

  def __init__(self, type, input_type, *args, **kwargs):
    fields = {name: field.type() for name, field in input_type._meta.fields.items()}
    kwargs.update(fields)
    super().__init__(type, *args, **kwargs)

  @classmethod
  def get_query(cls, model, info, sort=None, **args):
    query = super().get_query(model, info, sort=sort, **args)
    omitted = ('first', 'last', 'hasPreviousPage', 'hasNextPage', 'startCursor', 'endCursor')
    for name, val in args.items():
      if name in omitted: continue
      col = getattr(model, name, None)
      if col:
        query = query.filter(col == val)
        
    return query