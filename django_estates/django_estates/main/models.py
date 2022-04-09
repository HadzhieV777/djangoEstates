from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

UserModel = get_user_model()


class Estate(models.Model):
    TITLE_MAX_LEN = 100
    LOCATION_MAX_LEN = 150

    # Estate types
    ONE_BEDROOM_APARTMENT = 'One bedroom apartment'
    TWO_BEDROOMS_APARTMENT = 'Two bedrooms apartment'
    THREE_BEDROOMS_APARTMENT = 'Three bedrooms apartment'
    MAISONETTE = 'Maisonette'
    SINGLE_FAMILY_HOUSE = 'Single family house'
    DUPLEX = 'Duplex'
    VACATION_HOME = 'Vacation home'
    OFFICE = 'Office'
    HOTEL = 'Hotel'
    SPECIAL_PURPOSE = 'Special-purpose'
    INDUSTRIAL = 'Industrial'
    LAND = 'Land'

    ESTATE_TYPES = [(x, x) for x in (
        ONE_BEDROOM_APARTMENT, TWO_BEDROOMS_APARTMENT, THREE_BEDROOMS_APARTMENT, MAISONETTE, SINGLE_FAMILY_HOUSE,
        DUPLEX,
        VACATION_HOME, OFFICE, HOTEL, SPECIAL_PURPOSE, INDUSTRIAL, LAND)]

    # Floor types
    GROUND_FlOOR = 'Ground Floor'
    FIRST = '1st'
    SECOND = '2nd'
    THIRD = '3rd'
    FOURTH = '4th'
    FIFTH = '5th'
    SIXTH = '6th'
    SEVENTH = '7th'
    EIGHT = '8th'
    NINTH = '9th'
    TENTH = '10th'
    ELEVENTH = '11th'
    TWELFTH = '12th'
    THIRTEENTH = '13th'
    FOURTEENTH = '14th'
    FIFTEENTH = '15th'
    LAST_FLOOR = 'Last Floor'
    FLOOR_TYPES = [(x, x) for x in (GROUND_FlOOR, FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH,
                                    SEVENTH, EIGHT, NINTH, TENTH, ELEVENTH, TWELFTH, THIRTEENTH,
                                    FOURTEENTH, FIFTEENTH, LAST_FLOOR)]

    # Heating types
    FORCED_AIR_SYSTEMS = 'Forced Air System'
    STEAM_RADIANT_HEAT_SYSTEM = 'Steam Radiant Heat Systems'
    ELECTRIC_SYSTEM = 'Electric System'
    GEOTHERMAL_SYSTEM = 'Geothermal System'
    HEATING_TYPES = [(x, x) for x in
                     (FORCED_AIR_SYSTEMS, STEAM_RADIANT_HEAT_SYSTEM, ELECTRIC_SYSTEM, GEOTHERMAL_SYSTEM)]

    # Exposition types
    EAST = 'East'
    WEST = 'West'
    NORTH = 'North'
    SOUTH = 'South'
    EXSPOSITION_TYPES = [(x, x) for x in (EAST, WEST, NORTH, SOUTH)]

    DEFAULT_PRICE = 0
    PRICE_MIN_VALUE = 0

    # Type of transaction
    FOR_SALE = 'For sale'
    FOR_RENT = 'For rent'
    TYPES = [(x, x) for x in (FOR_SALE, FOR_RENT)]

    # Amenities
    AMENITIES_MAX_LENGTH = 200
    AMENITIES_REGEX = f'^[a-zA-Z]+(, [a-zA-Z]+)*$'
    AMENITIES_VALIDATOR_ERROR = "The ingredients should be separated by ', '."

    DESCRIPTION_MAX_LEN = 500

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )
    type = models.CharField(
        max_length=max(len(x) for (x, _) in ESTATE_TYPES),
        choices=ESTATE_TYPES,
    )
    location = models.CharField(
        max_length=LOCATION_MAX_LEN
    )
    floor = models.CharField(
        max_length=max(len(x) for (x, _) in FLOOR_TYPES),
        choices=FLOOR_TYPES,
    )
    heating_type = models.CharField(
        max_length=max(len(x) for (x, _) in HEATING_TYPES),
        choices=HEATING_TYPES,
    )
    area = models.FloatField()
    exposition = models.CharField(
        max_length=max(len(x) for (x, _) in EXSPOSITION_TYPES),
        choices=EXSPOSITION_TYPES,
    )
    price = models.FloatField(
        default=DEFAULT_PRICE,
        validators=(
            MinValueValidator(PRICE_MIN_VALUE),
        ),
    )
    type_of_transaction = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )
    description = models.TextField(
        max_length=DESCRIPTION_MAX_LEN,
    )
    amenities = models.CharField(
        max_length=AMENITIES_MAX_LENGTH,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=AMENITIES_REGEX,
                message=AMENITIES_VALIDATOR_ERROR,
            )
        ],
    )
    favourites = models.ManyToManyField(
        UserModel,
        related_name='favourite',
        default=None,
        blank=True,
    )
    main_image = models.ImageField()
    publication_date = models.DateField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title} {self.type} {self.price}'

    class Meta:
        ordering = ('publication_date',)


class EstateImages(models.Model):
    IMAGE_UPLOAD_TO_DIR = 'estates/'

    estate = models.ForeignKey(
        Estate,
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.FileField(
        upload_to=IMAGE_UPLOAD_TO_DIR,
    )
