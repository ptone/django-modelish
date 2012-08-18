django-modelish
===============

.. pull-quote::
    Because programmers are lazy...

Modelish is a quick attempt to save a few keystrokes. Many data modeling tools
are a GUI nightmare, with dropdowns and lots of buttons. But sometimes,
especially when you are sketching something out, writing out full Django models
can be a bit tedious.

Modelish will parse a file with a simplified model declaration in a flavor of
YAML and generate Python code for model definition.

Normally I would say source code generation is a "Bad Idea", but really even
in Python, Django models are a mostly declarative syntax


Quickstart
----------

Install django-predicate:

.. code-block:: console

    pip install django-modelish

You can then start banging out models like this

.. code-block:: yaml

    Poll:
        doc: This is the poll model
        question:
            type: char
            max_length: 200
        pub_date:
            type: datetime
            args: date published

    Choice:
        poll:
            type: fk
            args: [Poll]
        choice_text-char:
            max_length: 200
        votes:
            type: int

You then just use the CLI tool:

.. code-block:: console

    modelish path-to-file.yml

This will generate code like this:

.. code-block:: python

    class Poll(models.Model):
        """This is the poll model"""

        pub_date = models.DateTimeField(
            'date published')
        question = models.CharField(
            max_length=200,
            blank=True)

    class Choice(models.Model):
        choice_text = models.CharField(
            max_length=200,
            blank=True)
        poll = models.ForeignKey(
            'Poll')
        votes = models.IntegerField()

Syntax
------

The syntax is pretty simple::

    <ModelName>:
        [doc: docstring]
        <fieldname>[-type-alias]:
            [type: type-alias],
            [args: arglist],
            kwarg: value

The field type is represented by a shortened 'type' alias so 'char' becomes
'models.CharField' etc (see grammarish below).

The type can be specified one of two ways, either following the field name with
a hyphen, or explicitly declared as a ``type`` in the field definition.

Positional args to the model specified as an explicit list in square brackets,
or as a comma delimited string.

The remaining block of the field definition consists of kwarg/value pairs.

Working with grammarish
-----------------------

Modelish works with a grammar composed of type aliases and defaults. The standard
types are:

.. code-block:: yaml

    auto: AutoField
    bigint: BigIntegerField
    bool: BooleanField
    char: CharField
    date: DateField
    datetime: DateTimeField
    decimal: DecimalField
    email: EmailField
    file: FileField
    float: FloatField
    image: ImageField
    int: IntegerField
    ip: IPAddressField
    gip: GenericIPAddressField
    nbool: NullBooleanField
    pint: PositiveIntegerField
    psint: PositiveSmallIntegerField
    slug: SlugField
    sint: SmallIntegerField
    text: TextField
    time: TimeField
    url: URLField
    fk: ForeignKey
    m2m: ManyToManyField
    timestamp: DateTimeField

For each type - a set of default kwargs is defined in the grammar as
``defaults``:

.. code-block:: yaml

    defaults:
    bool:
        default: true
    char:
        max_length: 100
        blank: true
    nbool:
        null: true
    timestamp:
        auto-now: true

This default grammar can be replace, or enhanced by passing your own yaml files
to the command.  Use ``--grammar`` to replace the default grammer, and use
``--extra-grammar`` to merge in and update the default grammer with your own
additions or changes.

That's it - this isn't meant to be any sort of full featured model builder or
data modeler, it is just a simple DSLish bootstrap tool to give you
a models.py starting point with a little less typing.
