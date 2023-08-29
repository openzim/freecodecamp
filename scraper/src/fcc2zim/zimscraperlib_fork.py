from zimscraperlib.constants import (
    MAXIMUM_DESCRIPTION_METADATA_LENGTH as MAX_DESC_LENGTH,
)
from zimscraperlib.constants import (
    MAXIMUM_LONG_DESCRIPTION_METADATA_LENGTH as MAX_LONG_DESC_LENGTH,
)

# This function will be released in zimscraperlib 3.1.2
# Until then, it is forked here for convenience


def compute_descriptions(
    default_description: str,
    user_description: str | None,
    user_long_description: str | None,
) -> tuple[str, str | None]:
    """Computes short and long descriptions compliant with ZIM standard.

    Based on provided parameters, the function computes a short and a long description
    which are compliant with the ZIM standard (in terms of length).

    User description(s) are used if set. They are checked to not exceed ZIM standard
    maximum length ; an error is thrown otherwise ; if ok, they are returned.

    If user_description is not set, the description is computed based on the default
    description, truncated if needed.

    If user_long_description is not set and default description is too long for the
    description field, the long_description is computed based on the default description
    (truncated if needed), otherwise no long description is returned.

    args:
        default_description:   the description which will be used if user descriptions
                               are not set (typically fetched online)
        user_description:      the description set by the user (typically set by a
                               CLI argument)
        user_long_description: the long description set by the user (typically set by a
                               CLI argument)

    Returns a tuple of (description, long_description)
    """

    if user_description and len(user_description) > MAX_DESC_LENGTH:
        raise ValueError(
            f"Description too long ({len(user_description)}>{MAX_DESC_LENGTH})"
        )
    if user_long_description and len(user_long_description) > MAX_LONG_DESC_LENGTH:
        raise ValueError(
            f"LongDescription too long ({len(user_long_description)}"
            f">{MAX_LONG_DESC_LENGTH})"
        )

    if not user_long_description and len(default_description) > MAX_DESC_LENGTH:
        user_long_description = default_description[0:MAX_LONG_DESC_LENGTH]
        if len(default_description) > MAX_LONG_DESC_LENGTH:
            user_long_description = user_long_description[:-1] + "…"
    if not user_description:
        user_description = default_description[0:MAX_DESC_LENGTH]
        if len(default_description) > MAX_DESC_LENGTH:
            user_description = user_description[:-1] + "…"

    return (user_description, user_long_description)
