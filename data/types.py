from enum import StrEnum


class FundStatus(StrEnum):
    FUNDRAISING = "Fundraising"
    INVESTING = "Investing"
    CLOSED = "Closed"


class InvestorType(StrEnum):
    INDIVIDUAL = "Individual"
    INSTITUTION = "Institution"
    FAMILY_OFFICE = "FamilyOffice"
