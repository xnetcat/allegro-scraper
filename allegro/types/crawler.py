from typing import List, Literal, Optional, TypedDict


class Parameters(TypedDict):
    smart_free_shipping: Optional[bool]
    product_condition: Optional[
        List[
            Literal[
                "new",
                "used",
                "incomplete_set",
                "new_without_tags",
                "new_with_defect",
                "after_return",
                "aftermarket",
                "regenerated",
                "damaged",
                "refurbished",
                "for_renovation",
                "not_requiring_renovation",
            ]
        ]
    ]
    offer_type: Optional[List[Literal["buy_now", "auction", "advertisement"]]]
    price_min: Optional[float]
    price_max: Optional[float]
    delivery_time: Optional[Literal["today", "one_day", "two_day"]]
    delivery_methods: Optional[
        List[
            Literal[
                "courier",
                "inpost_parcel_locker",
                "overseas_delivery",
                "pickup_at_the_point",
                "letter",
                "package",
                "pickup",
                "email",
            ]
        ]
    ]
    delivery_options: Optional[List[Literal["free_shipping", "free_return"]]]
