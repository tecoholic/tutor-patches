KNOWN_MFES = frozenset({
    "all",
    "account",
    "authn",
    "communications",
    "authoring",
    "discussions",
    "gradebook",
    "learner-dashboard",
    "learning",
    "ora-grading",
    "profile",
})


def validate_mfe(mfe: str) -> str:
    """
    Validate MFE name.

    Returns the mfe name if valid, raises ValueError otherwise.
    Note: Only warns for unknown MFEs since custom MFEs are allowed.
    """
    if mfe not in KNOWN_MFES:
        import warnings

        warnings.warn(
            f"Unknown MFE '{mfe}'. Known MFEs: {sorted(KNOWN_MFES - {'all'})}. "
            "If this is a custom MFE, you can ignore this warning.",
            UserWarning,
            stacklevel=3,
        )
    return mfe
