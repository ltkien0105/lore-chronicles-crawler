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


class ContentPanelCardRegion(BaseModel):
    slug: str
    disabled: bool
    on_click_events: List[OnClickEvent] = Field(..., alias="onClickEvents")
    background_image: str = Field(..., alias="backgroundImage")
    title: str
    subtitle: str


class ContentPanelCard(BaseModel):
    bilgewater_architecture: ContentPanelCardRegion
    bilgewater_critters: ContentPanelCardRegion
    bilgewater_culture: ContentPanelCardRegion
    bilgewater_hunting: ContentPanelCardRegion
    bilgewater_nagakabouros: ContentPanelCardRegion
    bilgewater_people: ContentPanelCardRegion
    bilgewater_serpentisles: ContentPanelCardRegion
    bilgewater_slaughterdocks: ContentPanelCardRegion
    bilgewater_thecity: ContentPanelCardRegion
    bilgewater_tools: ContentPanelCardRegion
    demacia_architecture: ContentPanelCardRegion
    demacia_military: ContentPanelCardRegion
    demacia_plaza: ContentPanelCardRegion
    demacia_raptors: ContentPanelCardRegion
    demacia_silvermere: ContentPanelCardRegion
    freljord_architecture: ContentPanelCardRegion
    freljord_citadel: ContentPanelCardRegion
    freljord_glaseport: ContentPanelCardRegion
    freljord_people: ContentPanelCardRegion
    freljord_rakelstake: ContentPanelCardRegion
    freljord_tools: ContentPanelCardRegion
    ionia_architecture: ContentPanelCardRegion
    ionia_creatures: ContentPanelCardRegion
    ionia_culture: ContentPanelCardRegion
    ionia_environment: ContentPanelCardRegion
    ionia_flora: ContentPanelCardRegion
    ionia_people: ContentPanelCardRegion
    ionia_placidium: ContentPanelCardRegion
    ionia_rocks: ContentPanelCardRegion
    ionia_tools: ContentPanelCardRegion
    ionia_kinkou: ContentPanelCardRegion
    noxus_bastion: ContentPanelCardRegion
    noxus_creatures: ContentPanelCardRegion
    noxus_culture: ContentPanelCardRegion
    noxus_expansion: ContentPanelCardRegion
    noxus_legion: ContentPanelCardRegion
    noxus_shurima: ContentPanelCardRegion
    noxus_warbands: ContentPanelCardRegion
    piltover_architecture: ContentPanelCardRegion
    piltover_culture: ContentPanelCardRegion
    piltover_environment: ContentPanelCardRegion
    piltover_hextech: ContentPanelCardRegion
    piltover_people: ContentPanelCardRegion
    piltover_tools: ContentPanelCardRegion
    piltover_zaun: ContentPanelCardRegion
    shadow_architecture: ContentPanelCardRegion
    shadow_entities: ContentPanelCardRegion
    shadow_environment: ContentPanelCardRegion
    shadow_harrowing: ContentPanelCardRegion
    shadow_runination: ContentPanelCardRegion
    shurima_cascade: ContentPanelCardRegion
    shurima_dormun: ContentPanelCardRegion
    shurima_marrowmark: ContentPanelCardRegion
    shurima_nashramae: ContentPanelCardRegion
    shurima_noxus: ContentPanelCardRegion
    shurima_people: ContentPanelCardRegion
    shurima_sandswimmers: ContentPanelCardRegion
    shurima_sun: ContentPanelCardRegion
    shurima_valley: ContentPanelCardRegion
    shurima_zuretta: ContentPanelCardRegion
    targon_architecture: ContentPanelCardRegion
    targon_ascent: ContentPanelCardRegion
    targon_creature: ContentPanelCardRegion
    targon_impossible: ContentPanelCardRegion
    targon_lunari: ContentPanelCardRegion
    targon_peak: ContentPanelCardRegion
    targon_rakkor: ContentPanelCardRegion
    targon_ring: ContentPanelCardRegion
    targon_solari: ContentPanelCardRegion
    targon_tools: ContentPanelCardRegion
    void_environment: ContentPanelCardRegion
    void_history: ContentPanelCardRegion
    void_voidborn: ContentPanelCardRegion
    yordle_portals: ContentPanelCardRegion
    zaun_architecture: ContentPanelCardRegion
    zaun_baron: ContentPanelCardRegion
    zaun_entersol: ContentPanelCardRegion
    zaun_environment: ContentPanelCardRegion
    zaun_promenade: ContentPanelCardRegion
    zaun_punks: ContentPanelCardRegion
    zaun_sumps: ContentPanelCardRegion
    zaun_tools: ContentPanelCardRegion
    vathcaer_warmother: ContentPanelCardRegion
    ghulfrost_warmother: ContentPanelCardRegion
    ornnkaal_rocks_warmother: ContentPanelCardRegion
    quchar_warmother: ContentPanelCardRegion
    yadulsk_warmother: ContentPanelCardRegion
    ryze_short_pt3: ContentPanelCardRegion
    ryze_short_pt2: ContentPanelCardRegion
    ryze_short_pt1: ContentPanelCardRegion
    ryze_comic_pt1: ContentPanelCardRegion
    ryze_comic_pt2: ContentPanelCardRegion
    ryze_comic_pt3: ContentPanelCardRegion
    ryze_comic_pt4: ContentPanelCardRegion
    ryze_comic_pt5: ContentPanelCardRegion
    ryzecg_featured: ContentPanelCardRegion
    ryze_cg_pt1: ContentPanelCardRegion
    ryze_cg_pt3: ContentPanelCardRegion
    ryze_cg_pt4: ContentPanelCardRegion
    ryze_cg_pt5: ContentPanelCardRegion
    ryze_cg_pt6: ContentPanelCardRegion
    ryze_cg_pt7: ContentPanelCardRegion
    ryze_cg_pt8: ContentPanelCardRegion
    ezrealnotes_featured: ContentPanelCardRegion
    junglestory_featured: ContentPanelCardRegion
    jungle_daySTART: ContentPanelCardRegion
    jungle_day1: ContentPanelCardRegion
    jungle_day2: ContentPanelCardRegion
    jungle_day3: ContentPanelCardRegion
    jungle_day4: ContentPanelCardRegion
    ezreal_peretha: ContentPanelCardRegion
    ezreal_oshra: ContentPanelCardRegion
    jungle_neekoGallery: ContentPanelCardRegion
    jungle_nidaleeGallery: ContentPanelCardRegion
    antathir: ContentPanelCardRegion
    aurma: ContentPanelCardRegion
    basilich: ContentPanelCardRegion
    belzhun: ContentPanelCardRegion
    bilgewater_bay: ContentPanelCardRegion = Field(..., alias="bilgewater-bay")
    bloodcliffs: ContentPanelCardRegion
    boleham: ContentPanelCardRegion
    delverhold: ContentPanelCardRegion
    drekan: ContentPanelCardRegion
    drugne: ContentPanelCardRegion
    edessa: ContentPanelCardRegion
    evenmoor: ContentPanelCardRegion
    faelor: ContentPanelCardRegion
    fallgren: ContentPanelCardRegion
    fossbarrow: ContentPanelCardRegion
    frostheld: ContentPanelCardRegion
    gates_of_mourning: ContentPanelCardRegion = Field(..., alias="gates-of-mourning")
    ghulfrost: ContentPanelCardRegion
    glaserport: ContentPanelCardRegion
    glorft: ContentPanelCardRegion
    high_silvermere: ContentPanelCardRegion = Field(..., alias="high-silvermere")
    hirana_monastery: ContentPanelCardRegion = Field(..., alias="hirana-monastery")
    holdrum: ContentPanelCardRegion
    ironwater: ContentPanelCardRegion
    jandelle: ContentPanelCardRegion
    kalamanda: ContentPanelCardRegion
    kashuri: ContentPanelCardRegion
    kenethet: ContentPanelCardRegion
    khworez: ContentPanelCardRegion
    kilgrove: ContentPanelCardRegion
    kinkou_monastery: ContentPanelCardRegion = Field(..., alias="kinkou-monastery")
    krexor: ContentPanelCardRegion
    kumangra: ContentPanelCardRegion
    lissus: ContentPanelCardRegion
    master_yi_village: ContentPanelCardRegion = Field(..., alias="master-yi-village")
    mudtown: ContentPanelCardRegion
    nashramae: ContentPanelCardRegion
    needlebrook: ContentPanelCardRegion
    nerimazeth: ContentPanelCardRegion
    old_bargate: ContentPanelCardRegion = Field(..., alias="old-bargate")
    palclyff: ContentPanelCardRegion
    piltover_town: ContentPanelCardRegion = Field(..., alias="piltover-town")
    pinara: ContentPanelCardRegion
    puboe: ContentPanelCardRegion
    qualthala: ContentPanelCardRegion
    raikkon: ContentPanelCardRegion
    rakelstake: ContentPanelCardRegion
    rokrund: ContentPanelCardRegion
    ruug: ContentPanelCardRegion
    stonewall: ContentPanelCardRegion
    temple_jagged_knife: ContentPanelCardRegion = Field(
        ..., alias="temple-jagged-knife"
    )
    temple_pallas: ContentPanelCardRegion = Field(..., alias="temple-pallas")
    terbisia: ContentPanelCardRegion
    tereshni: ContentPanelCardRegion
    tevasa: ContentPanelCardRegion
    the_dawnhold: ContentPanelCardRegion = Field(..., alias="the-dawnhold")
    the_drakkengate: ContentPanelCardRegion = Field(..., alias="the-drakkengate")
    the_iron_pinnacle: ContentPanelCardRegion = Field(..., alias="the-iron-pinnacle")
    trannit: ContentPanelCardRegion
    trevale: ContentPanelCardRegion
    tuula: ContentPanelCardRegion
    urzeris: ContentPanelCardRegion
    uwendale: ContentPanelCardRegion
    vaskasia: ContentPanelCardRegion
    vathcaer: ContentPanelCardRegion
    vekaura: ContentPanelCardRegion
    velorus: ContentPanelCardRegion
    village_of_the_ice_children: ContentPanelCardRegion = Field(
        ..., alias="village-of-the-ice-children"
    )
    vindor: ContentPanelCardRegion
    vlonquo: ContentPanelCardRegion
    wrenwall: ContentPanelCardRegion
    zaun_town: ContentPanelCardRegion = Field(..., alias="zaun-town")
    zhyunia: ContentPanelCardRegion
    zirima: ContentPanelCardRegion
    zuretta: ContentPanelCardRegion
    ryganns_reach: ContentPanelCardRegion = Field(..., alias="ryganns-reach")
    valars_hollow: ContentPanelCardRegion = Field(..., alias="valars-hollow")
    marrowmark_market: ContentPanelCardRegion = Field(..., alias="marrowmark-market")
    the_city_of_gardens: ContentPanelCardRegion = Field(
        ..., alias="the-city-of-gardens"
    )
    yetis_vigil: ContentPanelCardRegion = Field(..., alias="yetis-vigil")
    foundling_village: ContentPanelCardRegion = Field(..., alias="foundling-village")
    naljaag: ContentPanelCardRegion
    wehle: ContentPanelCardRegion
    harelport: ContentPanelCardRegion
    paretha: ContentPanelCardRegion
    ornnkaal_rocks: ContentPanelCardRegion = Field(..., alias="ornnkaal-rocks")
    yadulsk: ContentPanelCardRegion
    quchar: ContentPanelCardRegion
    ixtal_region: ContentPanelCardRegion
    ixaocan_region: ContentPanelCardRegion
