class EduOrbParcipiant:
    def __init__(self, parcipiant_id, phpsessid):
        self.parcipiant_id: str = parcipiant_id
        self.phpsessid: str = phpsessid

    def get_cookies_with_phpsessid(self):
        return {"PHPSESSID": f"{self.phpsessid}"}
