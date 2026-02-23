from typing import List, Optional
from pydantic import BaseModel, Field


class Link(BaseModel):
    url: str
    label: str


class Fact(BaseModel):
    label: str
    description: str


class InteractionEvent(BaseModel):
    type: str
    slug: Optional[str] = None


class OnToastSelectEvent(InteractionEvent):
    zoom_level: int | None = Field(None, alias="zoomLevel")
    slugs: Optional[List[str]] = None
    value: Optional[bool] = None


class OnClickEvent(InteractionEvent):
    desktop_only: bool | None = Field(None, alias="desktopOnly")
    mobile_only: bool | None = Field(None, alias="mobileOnly")
    delay: int | None = Field(None)
    zoom_level: int | None = Field(None, alias="zoomLevel")


class OnContentPanelOpen(OnToastSelectEvent):
    pass


class ActionBar(BaseModel):
    type: str
    icon_type: str | None = Field(None, alias="iconType")
    label: Optional[str] = None
    position: str
    onClickEvents: List[OnClickEvent] | None = Field(None, alias="onClickEvents")


class ContentPanelRegion(BaseModel):
    slug: str
    disabled: bool
    card_slugs: List[str] | None = Field(None, alias="cardSlugs")
    crest_image: Optional[str] | List[str] = Field(None, alias="crestImage")
    toast_background: str = Field(..., alias="toastBackground")
    flyout_background: str = Field(..., alias="flyoutBackground")
    background_image: str = Field(..., alias="backgroundImage")
    title: str
    subtitle: str
    description: Optional[str] = None
    link: Optional[Link] = None
    facts: Optional[List[Fact]] = None
    champion_slugs: List[str] | None = Field(None, alias="championSlugs")
    action_bar: List[ActionBar] | None = Field(None, alias="actionBar")
    on_toast_select_events: List[OnToastSelectEvent] = Field(
        ..., alias="onToastSelectEvents"
    )
    on_content_panel_open: List[OnContentPanelOpen] | None = Field(
        None, alias="onContentPanelOpen"
    )


class ContentPanel(BaseModel):
    bilgewater: ContentPanelRegion
    demacia: ContentPanelRegion
    freljord: ContentPanelRegion
    icathia: ContentPanelRegion
    ionia: ContentPanelRegion
    ixtal: ContentPanelRegion
    noxus: ContentPanelRegion
    piltover_zaun: ContentPanelRegion = Field(..., alias="piltover-zaun")
    shadow_isles: ContentPanelRegion = Field(..., alias="shadow-isles")
    shurima: ContentPanelRegion
    targon: ContentPanelRegion
    sun_disc: ContentPanelRegion = Field(..., alias="sun-disc")
    immortal_bastion: ContentPanelRegion = Field(..., alias="immortal-bastion")
    ixaocan: ContentPanelRegion
    mount_targon: ContentPanelRegion = Field(..., alias="mount-targon")
    demacia_city_landmark: ContentPanelRegion = Field(
        ..., alias="demacia-city-landmark"
    )
    frostguard: ContentPanelRegion
    placidium: ContentPanelRegion
    bandle_city: ContentPanelRegion = Field(..., alias="bandle-city")
    the_void: ContentPanelRegion = Field(..., alias="the-void")
    basilich: ContentPanelRegion
    belzhun: ContentPanelRegion
    bilgewater_bay: ContentPanelRegion = Field(..., alias="bilgewater-bay")
    delverhold: ContentPanelRegion
    fossbarrow: ContentPanelRegion
    frostheld: ContentPanelRegion
    glaserport: ContentPanelRegion
    ghulfrost: ContentPanelRegion
    high_silvermere: ContentPanelRegion = Field(..., alias="high-silvermere")
    hirana_monastery: ContentPanelRegion = Field(..., alias="hirana-monastery")
    kinkou_monastery: ContentPanelRegion = Field(..., alias="kinkou-monastery")
    nashramae: ContentPanelRegion
    ornnkaal_rocks: ContentPanelRegion = Field(..., alias="ornnkaal-rocks")
    piltover_town: ContentPanelRegion = Field(..., alias="piltover-town")
    rakelstake: ContentPanelRegion
    temple_pallas: ContentPanelRegion = Field(..., alias="temple-pallas")
    trevale: ContentPanelRegion
    uwendale: ContentPanelRegion
    zaun_town: ContentPanelRegion = Field(..., alias="zaun-town")
    zirima: ContentPanelRegion
    ryganns_reach: ContentPanelRegion = Field(..., alias="ryganns-reach")
    valars_hollow: ContentPanelRegion = Field(..., alias="valars-hollow")
    marrowmark_market: ContentPanelRegion = Field(..., alias="marrowmark-market")
    the_city_of_gardens: ContentPanelRegion = Field(..., alias="the-city-of-gardens")
    yetis_vigil: ContentPanelRegion = Field(..., alias="yetis-vigil")
    foundling_village: ContentPanelRegion = Field(..., alias="foundling-village")
    naljaag: ContentPanelRegion
    vathcaer: ContentPanelRegion
    village_of_the_ice_children: ContentPanelRegion = Field(
        ..., alias="village-of-the-ice-children"
    )
    quchar: ContentPanelRegion
    yadulsk: ContentPanelRegion
    bilgewater_nagakabouros: ContentPanelRegion
    bilgewater_buhru: ContentPanelRegion
    bilgewater_warfrats: ContentPanelRegion
    bilgewater_hunting: ContentPanelRegion
    noxus_warbands: ContentPanelRegion
    noxus_expansion: ContentPanelRegion
    ionia_fauna: ContentPanelRegion
    ionia_flora: ContentPanelRegion
    targon_creature: ContentPanelRegion
    shadow_history: ContentPanelRegion
    ionian_rocks: ContentPanelRegion
    demacia_raptors: ContentPanelRegion
    shurima_dormun: ContentPanelRegion
    shurima_valley: ContentPanelRegion
    shurima_cascade: ContentPanelRegion
    shurima_sandswimmers: ContentPanelRegion
    shadow_harrowing: ContentPanelRegion
    shurima_noxus: ContentPanelRegion
    ryze_story_3: ContentPanelRegion
    ryze_comic_5: ContentPanelRegion
    ryze_comic_4: ContentPanelRegion
    featured: ContentPanelRegion
    ryzecg_featured: ContentPanelRegion
    ryze_cgi_1: ContentPanelRegion
    ryze_cgi_3: ContentPanelRegion
    ryze_cgi_4: ContentPanelRegion
    ryze_cgi_5: ContentPanelRegion
    ryze_cgi_6: ContentPanelRegion
    ryze_cgi_7: ContentPanelRegion
    ryze_cgi_8: ContentPanelRegion
    ezrealnotes_featured: ContentPanelRegion
    ezrealnotes1: ContentPanelRegion
    ezrealnotes2: ContentPanelRegion
    ezrealnotes3: ContentPanelRegion
    ezrealnotes4: ContentPanelRegion
    ezrealnotes5: ContentPanelRegion
    ezrealnotes6: ContentPanelRegion
    ezrealnotes7: ContentPanelRegion
    ezrealnotes8: ContentPanelRegion
    ezrealnotes9: ContentPanelRegion
    ezrealnotes10: ContentPanelRegion
    ezrealnotes11: ContentPanelRegion
    ezrealnotes12: ContentPanelRegion
    ezrealnotes13: ContentPanelRegion
    ezrealnotes14: ContentPanelRegion
    ezrealnotes15: ContentPanelRegion
    ezrealnotes16: ContentPanelRegion
    ezrealnotes17: ContentPanelRegion
    ezrealnotes18: ContentPanelRegion
    ezrealnotes19: ContentPanelRegion
    ezrealnotes20: ContentPanelRegion
    junglestory_featured: ContentPanelRegion
    jungle_day1: ContentPanelRegion
    jungle_day2: ContentPanelRegion
    jungle_day3: ContentPanelRegion
    jungle_day4: ContentPanelRegion
