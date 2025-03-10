# Description: Module de navigation
# Version: 1.0


def redirect_to_group(driver, facebook_group_url):
    """Redirige vers un groupe Facebook"""
    print(f"🔗 Redirection vers le groupe Facebook : {facebook_group_url}")
    driver.get(facebook_group_url)
