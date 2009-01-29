#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

#Code taken from
#http://www.djangosnippets.org/snippets/864/

from django.db import models

class Item(object):
    def __init__(self, value, slug, display=None):
        if not isinstance(value, int):
            raise TypeError('item value should be an integer, not %s' % value.__class__.__name__)
        if not isinstance(slug, str):
            raise TypeError('item slug should be a string, not %s' % slug.__class__.__name__)
        if display != None and not isinstance(display, (str)):
            raise TypeError('item slug should be a string, not %s' % display.__class__.__name__)
        super(Item, self).__init__()
        self.value = value
        self.slug = slug
        if display == None:
            self.display = slug
        else:
            self.display = display
        
    def __str__(self):
        return self.display
    
    def __repr__(self):
        return '<enum.Item: %s>' % self.display
    
    def __eq__(self, other):
        if isinstance(other, Item):
            return self.value == other.value        
        if isinstance(other, (int, str, unicode)):
            try:
                return self.value == int(other)
            except ValueError:
                return False        
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Enumeration(object):
    @classmethod
    def from_value(cls, value):
        for attr in cls.__dict__.values():
            if isinstance(attr, Item) and attr.value == value:
                return attr
    
    @classmethod
    def from_slug(cls, slug):
        for attr in cls.__dict__.values():
            if isinstance(attr, Item) and attr.slug == slug:
                return attr
    
    @classmethod
    def get_items(cls):
        items = filter(lambda attr: isinstance(attr, Item), cls.__dict__.values())
        items.sort(lambda x, y: cmp(x.value, y.value))
        return items

    @classmethod
    def get_choices(cls):
        return [(item.value, item.display.capitalize()) for item in cls.get_items()]


class EnumField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, enumeration, *args, **kwargs):
        kwargs.setdefault('choices', enumeration.get_choices())
        super(EnumField, self).__init__(*args, **kwargs)
        self.enumeration = enumeration
    
    def get_internal_type(self):
        return 'IntegerField'

    def to_python(self, value):
        if value == None or value == '' or value == u'':
            return None
        if isinstance(value, Item):
            return value
        if isinstance(value, int) or isinstance(value, str) or isinstance(value, unicode):
            item = self.enumeration.from_value(int(value))
            if item:
                return item
        
        raise ValueError, '%s is not a valid value for the enum field' % value
    
    
    def get_db_prep_save(self, value):
        if value:
            return value.value
    
    def get_db_prep_lookup(self, lookup_type, value):
        def prepare(value):
            if value == None:
                return None
            if isinstance(value, (int, str, unicode)):
                try:
                    return int(value)
                except ValueError:
                    raise ValueError('invalid value for the enum field lookup: %r' % value)
            if isinstance(value, Item):
                return value.value
        
        if lookup_type == 'exact':
            return [prepare(value)]
        elif lookup_type == 'in':
            return [prepare(v) for v in value]
        elif lookup_type == 'isnull':
            return []
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)
