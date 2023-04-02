import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
from tkinter import messagebox



class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Google-Analytics-BOT-JOURNEY")
        self.geometry("600x500")
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Crear opciones de menú
        self.menu_bar.add_command(label="Reportes", command=self.show_frame1)
        self.menu_bar.add_command(label="Journeys", command=self.show_frame2)
        self.menu_bar.add_command(label="Buscar Journeys", command=self.show_frame3)

        # Crear frames
        self.frame1 = tk.Frame(self, bg="white")
        self.frame2 = tk.Frame(self, bg="white")
        self.frame3 = tk.Frame(self, bg="white")

        # Mostrar el primer frame por defecto
        self.current_frame = None
        self.show_frame1()

    def show_frame1(self):
        self.show_frame(self.frame1, message="Hola")

        self.textbox = tk.Entry(self.frame1, font=("Arial", 10), bd=0, highlightthickness=1, highlightbackground="black")
        self.textbox.place(x=50, y=120, width=230)

        self.textbox2 = tk.Entry(self.frame1, font=("Arial", 10), bd=0, highlightthickness=1,
                                highlightbackground="black")
        self.textbox2.place(x=300, y=120, width=230)

        self.search_query = tk.StringVar()
        self.search_query2= tk.StringVar()

        self.textbox.config(textvariable=self.search_query)
        self.search_query.trace_add("write", lambda *args: self.filter_checkboxes_dim(self.search_query.get()))

        self.textbox2.config(textvariable=self.search_query2)
        self.search_query2.trace_add("write", lambda *args: self.filter_checkboxes_metricas(self.search_query2.get()))

        self.text_fechaIni = tk.Label(self.frame1, text="Fecha Ini.", bg='white', font=("Calibri", 12))
        self.text_fechaIni.place(x=50, y=30)

        self.texto_inf = tk.StringVar()
        rango_inf = DateEntry(self.frame1, width=20, background='black', foreground="white", bd=2,
                              textvariable=self.texto_inf, date_pattern='YYYY-MM-dd')
        rango_inf.place(x=130, y=30)

        self.text_fechaFin = tk.Label(self.frame1, text="Fecha Fin.", bg='white', font=("Calibri", 12))
        self.text_fechaFin.place(x=50, y=60)

        self.texto_sup = tk.StringVar()
        rango_sup = DateEntry(self.frame1, width=20, background='black', foreground="white", bd=1,
                              textvariable=self.texto_sup, date_pattern='YYYY-MM-dd')
        rango_sup.place(x=130, y=60)

        self.frame_izq = tk.Frame(self.frame1, bd=1, relief=tk.SUNKEN, bg="white")
        self.frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_der = tk.Frame(self.frame1, bd=1, relief=tk.SUNKEN, bg="white")
        self.frame_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas1 = tk.Canvas(self.frame_izq, bg="white")
        self.canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas2 = tk.Canvas(self.frame_der, bg="white")
        self.canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame1_checkbox_frame = tk.Frame(self.canvas1, bg="white")
        self.frame1_checkbox_frame.pack(fill=tk.BOTH, expand=True)

        self.frame2_checkbox_frame = tk.Frame(self.canvas2, bg="white")
        self.frame2_checkbox_frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame1, text="Dimensiones", bg='white', font=("Calibri", 12))
        self.label.place(x=50,y=90)
        self.frame_izq.place(x=50, y=150, width=230, height=300)

        self.label2 = tk.Label(self.frame1, text="Metricas", bg='white', font=("Calibri", 12))
        self.label2.place(x=300, y=90)
        self.frame_der.place(x=300, y=150, width=230, height=300)

        self.dimensiones = ['User Type',
 'Count of Sessions',
 'Days Since Last Session',
 'User Defined Value',
 'User Bucket',
 'Session Duration',
 'Referral Path',
 'Full Referrer',
 'Campaign',
 'Source',
 'Medium',
 'Source / Medium',
 'Keyword',
 'Ad Content',
 'Social Network',
 'Social Source Referral',
 'Campaign Code',
 'Google Ads: Ad Group ',
 'Google Ads: Ad Slot ',
 'Ad Distribution Network ',
 'Query Match Type ',
 'Keyword Match Type ',
 'Search Query ',
 'Placement Domain ',
 'Placement URL ',
 'Ad Format ',
 'Targeting Type ',
 'Placement Type ',
 'Display URL ',
 'Destination URL ',
 'Google Ads Customer ID ',
 'Google Ads Campaign ID ',
 'Google Ads Ad Group ID ',
 'Google Ads Creative ID ',
 'Google Ads Criteria ID ',
 'Query Word Count ',
 'TrueView Video Ad ',
 'Goal Completion Location ',
 'Goal Previous Step - 1 ',
 'Goal Previous Step - 2 ',
 'Goal Previous Step - 2 ',
 'Browser ',
 'Browser Version ',
 'Operating System ',
 'Operating System Version ',
 'Mobile Device Branding ',
 'Mobile Device Model ',
 'Mobile Input Selector',
 'Mobile Device Info ',
 'Mobile Device Marketing Name',
 'Device Category ',
 'Browser Size ',
 'Data Source ',
 'Continent',
 'Sub Continent ',
 'Country ',
 'Region ',
 'Metro ',
 'City ',
 'Latitude ',
 'Longitude ',
 'Network Domain ',
 'Service Provider ',
 'City ID ',
 'Continent ID',
 'Country ISO Code ',
 'Metro Id ',
 'Region ID ',
 'Region ISO Code ',
 'Sub Continent Code ',
 'Flash Version',
 'Java Support ',
 'Language ',
 'Screen Colors ',
 'Source Property Display Name ',
 'Source Property Tracking ID ',
 'Screen Resolution ',
 'Hostname ',
 'Page ',
 'Page path level 1 ',
 'Page path level 2 ',
 'Page path level 3',
 'Page path level 4',
 'Page Title ',
 'Landing Page',
 'Second Page ',
 'Exit Page ',
 'Previous Page Path ',
 'Page Depth ',
 'Landing Page Group XX ',
 'Previous Page Group XX',
 'Page Group XX ',
 'Site Search Status ',
 'Search Term ',
 'Refined Keyword',
 'Site Search Category ',
 'Start Page ',
 'Destination Page ',
 'Search Destination Page',
 'App Installer ID ',
 'App Version ',
 'App Name ',
 'App ID ',
 'Screen Name ',
 'Screen Depth ',
 'Landing Screen',
 'Exit Screen ',
 'Event Category ',
 'Event Action ',
 'Event Label ',
 'Transaction ID ',
 'Affiliation ',
 'Sessions to Transaction ',
 'Days to Transaction ',
 'Product SKU',
 'Product ',
 'Product Category ',
 'Currency Code',
 'Checkout Options ',
 'Internal Promotion Creative ',
 'Internal Promotion ID',
 'Internal Promotion Name ',
 'Internal Promotion Position ',
 'Order Coupon Code',
 'Product Brand ',
 'Product Category (Enhanced Ecommerce) ',
 'Product Category Level XX ',
 'Product Coupon Code ',
 'Product List Name ',
 'Product List Position',
 'Product Variant',
 'Shopping Stage ',
 'Social Network ',
 'Social Action ',
 'Social Network and Action (Hit)',
 'Social Entity ',
 'Social Type ',
 'Timing Category ',
 'Timing Label',
 'Timing Variable ',
 'ga:exceptionDescription ',
 'Experiment ID',
 'Variant ',
 'Experiment ID with Variant',
 'Experiment Name ',
 'Custom Dimension XX',
 'Custom Variable (Key XX) ',
 'Custom Variable (Value XX)',
 'Date',
 'Year ',
 'Month of the year ',
 'Week of the Year ',
 'Day of the month ',
 'Hour ',
 'Minute',
 'Month Index ',
 'Week Index ',
 'Day Index ',
 'Minute Index ',
 'Day of Week',
 'Day of Week Name',
 'Hour of Day ',
 'Date Hour and Minute',
 'Month of Year',
 'Week of Year ',
 'ISO Week of the Year ',
 'ISO Year ',
 'ISO Week of ISO Year ',
 'Hour Index ',
 'CM360 Ad (GA Model)',
 'CM360 Ad ID (GA Model)',
 'CM360 Ad Type (GA Model) ',
 'CM360 Ad Type ID ',
 'CM360 Advertiser (GA Model) ',
 'CM360 Advertiser ID (GA Model) ',
 'CM360 Campaign (GA Model) ',
 'CM360 Campaign ID (GA Model)',
 'CM360 Creative ID (GA Model) ',
 'CM360 Creative (GA Model) ',
 'CM360 Rendering ID (GA Model) ',
 'CM360 Creative Type (GA Model) ',
 'CM360 Creative Type ID (GA Model) ',
 'CM360 Creative Version (GA Model) ',
 'CM360 Site (GA Model) ',
 'CM360 Site ID (GA Model) ',
 'CM360 Placement (GA Model) ',
 'CM360 Placement ID (GA Model) ',
 'CM360 Floodlight Configuration ID (GA Model) ',
 'CM360 Activity ',
 'CM360 Activity and Group ',
 'CM360 Activity Group ',
 'CM360 Activity Group ID ',
 'CM360 Activity ID ',
 'CM360 Advertiser ID ',
 'CM360 Floodlight Configuration ID ',
 'CM360 Ad',
 'CM360 Ad ID (CM360 Model) ',
 'CM360 Ad Type (CM360 Model) ',
 'CM360 Ad Type ID (CM360 Model) ',
 'CM360 Advertiser (CM360 Model) ',
 'Age ',
 'Gender ',
 'Other Category ',
 'Affinity Category (reach) ',
 'Affinity Category (reach) ',
 'GAM Line Item Id',
 'GAM Line Item Name ',
 'Acquisition Campaign ',
 'Acquisition Medium ',
 'Acquisition Source',
 'Acquisition Source / Medium ',
 'Acquisition Channel',
 'Cohort',
 'Day ',
 'Month',
 'Week ',
 'Default Channel Grouping',
 'DV360 Advertiser (GA Model) ',
 'DV360 Advertiser ID (GA Model)',
 'DV360 Creative ID (GA Model) ',
 'DV360 Advertiser ID (GA Model)',
 'DV360 Exchange ID (GA Model) ',
 'DV360 Insertion Order (GA Model) ',
 'DV360 Insertion Order ID (GA Model)',
 'DV360 Line Item NAME (GA Model) ',
 'DV360 Line Item ID (GA Model) ',
 'DV360 Site (GA Model)',
 'DV360 Site ID (GA Model) ',
 'DV360 Advertiser (CM360 Model) ',
 'DV360 Advertiser ID (CM360 Model) ',
 'DV360 Creative ID (CM360 Model)',
 'DV360 Exchange (CM360 Model) ',
 'DV360 Exchange ID (CM360 Model) ',
 'DV360 Insertion Order (CM360 Model) ',
 'DV360 Insertion Order ID (CM360 Model) ',
 'DV360 Line Item (CM360 Model) ',
 'DV360 Line Item ID (CM360 Model) ',
 'DV360 Site (CM360 Model) ',
 'DV360 Site ID (CM360 Model)',
 'SA360 Ad Group ',
 'SA360 Ad Group ID ',
 'SA360 Advertiser ',
 'SA360 Advertiser ID ',
 'SA360 Agency ',
 'SA360 Agency ID ',
 'SA360 Campaign ',
 'SA360 Campaign ID',
 'SA360 Engine Account ',
 'SA360 Engine Account ID ',
 'SA360 Keyword',
 'SA360 Keyword ID']
        self.dimensiones_codigos=['ga:userType',
 'ga:sessionCount',
 'ga:daysSinceLastSession',
 'ga:userDefinedValue',
 'ga:userBucket',
 'ga:sessionDurationBucket',
 'ga:referralPath',
 'ga:fullReferrer',
 'ga:campaign',
 'ga:source',
 'ga:medium',
 'ga:sourceMedium',
 'ga:keyword',
 'ga:adContent',
 'ga:socialNetwork',
 'ga:hasSocialSourceReferral',
 'ga:campaignCode',
 'ga:adGroup',
 'ga:adSlot',
 'ga:adDistributionNetwork',
 'ga:adMatchType',
 'ga:adKeywordMatchType',
 'ga:adMatchedQuery',
 'ga:adPlacementDomain',
 'ga:adPlacementUrl',
 'ga:adFormat',
 'ga:adTargetingType',
 'ga:adTargetingOption',
 'ga:adDisplayUrl',
 'ga:adDestinationUrl',
 'ga:adwordsCustomerID',
 'ga:adwordsCampaignID',
 'ga:adwordsAdGroupID',
 'ga:adwordsCreativeID',
 'ga:adwordsCriteriaID',
 'ga:adQueryWordCount',
 'ga:isTrueViewVideoAd',
 'ga:goalCompletionLocation',
 'ga:goalPreviousStep1',
 'ga:goalPreviousStep2',
 'ga:goalPreviousStep3',
 'ga:browser',
 'ga:browserVersion',
 'ga:operatingSystem',
 'ga:operatingSystemVersion',
 'ga:mobileDeviceBranding',
 'ga:mobileDeviceModel',
 'ga:mobileInputSelector',
 'ga:mobileDeviceInfo',
 'ga:mobileDeviceMarketingName',
 'ga:deviceCategory',
 'ga:browserSize',
 'ga:dataSource',
 'ga:continent',
 'ga:subContinent',
 'ga:country',
 'ga:region',
 'ga:metro',
 'ga:city',
 'ga:latitude',
 'ga:longitude',
 'ga:networkDomain',
 'ga:networkLocation',
 'ga:cityId',
 'ga:continentId',
 'ga:countryIsoCode',
 'ga:metroId',
 'ga:regionId',
 'ga:regionIsoCode',
 'ga:subContinentCode',
 'ga:flashVersion',
 'ga:javaEnabled',
 'ga:language',
 'ga:screenColors',
 'ga:sourcePropertyDisplayName',
 'ga:sourcePropertyTrackingId',
 'ga:screenResolution',
 'ga:hostname',
 'ga:pagePath',
 'ga:pagePathLevel1',
 'ga:pagePathLevel2',
 'ga:pagePathLevel3',
 'ga:pagePathLevel4',
 'ga:pageTitle',
 'ga:landingPagePath',
 'ga:secondPagePath',
 'ga:exitPagePath',
 'ga:previousPagePath',
 'ga:pageDepth',
 'ga:landingContentGroupXX',
 'ga:previousContentGroupXX',
 'ga:contentGroupXX',
 'ga:searchUsed',
 'ga:searchKeyword',
 'ga:searchKeywordRefinement',
 'ga:searchCategory',
 'ga:searchStartPage',
 'ga:searchDestinationPage',
 'ga:searchAfterDestinationPage',
 'ga:appInstallerId',
 'ga:appVersion',
 'ga:appName',
 'ga:appId',
 'ga:screenName',
 'ga:screenDepth',
 'ga:landingScreenName',
 'ga:exitScreenName',
 'ga:eventCategory',
 'ga:eventAction',
 'ga:eventLabel',
 'ga:transactionId',
 'ga:affiliation',
 'ga:sessionsToTransaction',
 'ga:daysToTransaction',
 'ga:productSku',
 'ga:productName',
 'ga:productCategory',
 'ga:currencyCode',
 'ga:checkoutOptions',
 'ga:internalPromotionCreative',
 'ga:internalPromotionId',
 'ga:internalPromotionName',
 'ga:internalPromotionPosition',
 'ga:orderCouponCode',
 'ga:productBrand',
 'ga:productCategoryHierarchy',
 'ga:productCategoryLevelXX',
 'ga:productCouponCode',
 'ga:productListName',
 'ga:productListPosition',
 'ga:productVariant',
 'ga:shoppingStage',
 'ga:socialInteractionNetwork',
 'ga:socialInteractionAction',
 'ga:socialInteractionNetworkAction',
 'ga:socialInteractionTarget',
 'ga:socialEngagementType',
 'ga:userTimingCategory',
 'ga:userTimingLabel',
 'ga:userTimingVariable',
 'ga:exceptionDescription',
 'ga:experimentId',
 'ga:experimentVariant',
 'ga:experimentCombination',
 'ga:experimentName',
 'ga:dimensionXX',
 'ga:customVarNameXX',
 'ga:customVarValueXX',
 'ga:date',
 'ga:year',
 'ga:month',
 'ga:week',
 'ga:day',
 'ga:hour',
 'ga:minute',
 'ga:nthMonth',
 'ga:nthWeek',
 'ga:nthDay',
 'ga:nthMinute',
 'ga:dayOfWeek',
 'ga:dayOfWeekName',
 'ga:dateHour',
 'ga:dateHourMinute',
 'ga:yearMonth',
 'ga:yearWeek',
 'ga:isoWeek',
 'ga:isoYear',
 'ga:isoYearIsoWeek',
 'ga:nthHour',
 'ga:dcmClickAd',
 'ga:dcmClickAdId',
 'ga:dcmClickAdType',
 'ga:dcmClickAdTypeId',
 'ga:dcmClickAdvertiser',
 'ga:dcmClickAdvertiserId',
 'ga:dcmClickCampaign',
 'ga:dcmClickCampaignId',
 'ga:dcmClickCreativeId',
 'ga:dcmClickCreative',
 'ga:dcmClickRenderingId',
 'ga:dcmClickCreativeType',
 'ga:dcmClickCreativeTypeId',
 'ga:dcmClickCreativeVersion',
 'ga:dcmClickSite',
 'ga:dcmClickSiteId',
 'ga:dcmClickSitePlacement',
 'ga:dcmClickSitePlacementId',
 'ga:dcmClickSpotId',
 'ga:dcmFloodlightActivity',
 'ga:dcmFloodlightActivityAndGroup',
 'ga:dcmFloodlightActivityGroup',
 'ga:dcmFloodlightActivityGroupId',
 'ga:dcmFloodlightActivityId',
 'ga:dcmFloodlightAdvertiserId',
 'ga:dcmFloodlightSpotId',
 'ga:dcmLastEventAd',
 'ga:dcmLastEventAdId',
 'ga:dcmLastEventAdType',
 'ga:dcmLastEventAdTypeId',
 'ga:dcmLastEventAdvertiser',
 'ga:userAgeBracket',
 'ga:userGender',
 'ga:interestOtherCategory',
 'ga:interestAffinityCategory',
 'ga:interestInMarketCategory',
 'ga:dfpLineItemId',
 'ga:dfpLineItemName',
 'ga:acquisitionCampaign',
 'ga:acquisitionMedium',
 'ga:acquisitionSource',
 'ga:acquisitionSourceMedium',
 'ga:acquisitionTrafficChannel',
 'ga:cohort',
 'ga:cohortNthDay',
 'ga:cohortNthMonth',
 'ga:cohortNthWeek',
 'ga:channelGrouping',
 'ga:dbmClickAdvertiser',
 'ga:dbmClickAdvertiserId',
 'ga:dbmClickCreativeId',
 'ga:dbmClickExchange',
 'ga:dbmClickExchangeId',
 'ga:dbmClickInsertionOrder',
 'ga:dbmClickInsertionOrderId',
 'ga:dbmClickLineItem',
 'ga:dbmClickLineItemId',
 'ga:dbmClickSite',
 'ga:dbmClickSiteId',
 'ga:dbmLastEventAdvertiser',
 'ga:dbmLastEventAdvertiserId',
 'ga:dbmLastEventCreativeId',
 'ga:dbmLastEventExchange',
 'ga:dbmLastEventExchangeId',
 'ga:dbmLastEventInsertionOrder',
 'ga:dbmLastEventInsertionOrderId',
 'ga:dbmLastEventLineItem',
 'ga:dbmLastEventLineItemId',
 'ga:dbmLastEventSite',
 'ga:dbmLastEventSiteId',
 'ga:dsAdGroup',
 'ga:dsAdGroupId',
 'ga:dsAdvertiser',
 'ga:dsAdvertiserId',
 'ga:dsAgency',
 'ga:dsAgencyId',
 'ga:dsCampaign',
 'ga:dsCampaignId',
 'ga:dsEngineAccount',
 'ga:dsEngineAccountId',
 'ga:dsKeyword',
 'ga:dsKeywordId']
        self.dimensiones_seleccionadas=[]
        self.metricas=['Users',
 'New Users',
 '% New Sessions',
 '1 Day Active Users',
 '7 Day Active Users',
 '14 Day Active Users',
 '30 Day Active Users',
 'Number of Sessions per User',
 'Sessions',
 'Bounces',
 'Bounce Rate',
 'Session Duration',
 'Avg. Session Duration',
 'Unique Dimension Combinations',
 'Hits',
 'Organic Searches',
 'Impressions ',
 'Clicks ',
 'Cost ',
 'CPM',
 'CPC',
 'CTR ',
 'Cost per Transaction ',
 'Cost per Goal Conversion ',
 'Cost per Conversion ',
 'RPC ',
 'ROAS ',
 'Goal XX Starts ',
 'Goal Starts ',
 'Goal XX Completions ',
 'Goal Completions ',
 'Goal XX Value ',
 'Goal Value ',
 'Per Session Goal Value ',
 'Goal XX Conversion Rate ',
 'Goal Conversion Rate ',
 'Goal XX Abandoned Funnels ',
 'Abandoned Funnels ',
 'Goal XX Abandonment Rate ',
 'Total Abandonment Rate',
 'Page Value',
 'Entrances ',
 'Entrances / Pageviews ',
 'Entrances / Pageviews ',
 'Pages / Session ',
 'Unique Pageviews ',
 'Time on Page ',
 'Avg. Time on Page ',
 'Exits ',
 '% Exit ',
 'Custom Dimension XX',
 'Custom Variable (Key XX) ',
 'Custom Variable (Value XX)',
 'Previous Page Group XX',
 'Date',
 'Year ',
 'Month of the year ',
 'Week of the Year ',
 'Day of the month ',
 'Hour ',
 'Minute',
 'Month Index ',
 'Week Index ',
 'Day Index ',
 'Minute Index ',
 'Day of Week',
 'Day of Week Name',
 'Hour of Day ',
 'Date Hour and Minute',
 'Month of Year',
 'Week of Year ',
 'ISO Week of the Year ',
 'ISO Year ',
 'ISO Week of ISO Year ',
 'Hour Index ',
 '% Search Refinements ',
 'Time after Search ',
 'Time after Search ',
 'Search Exits ',
 '% Search Exits ',
 'Site Search Goal XX Conversion Rate ',
 'Site Search Goal Conversion Rate ',
 'Per Search Goal Value ',
 'Page Load Time (ms) ',
 'Page Load Sample',
 'Avg. Page Load Time (sec)',
 'Domain Lookup Time (ms) ',
 'Avg. Domain Lookup Time (sec)',
 'Page Download Time (ms) ',
 'Avg. Page Download Time (sec)',
 'Redirection Time (ms)',
 'Avg. Redirection Time (sec) ',
 'Server Connection Time (ms)',
 'Avg. Server Connection Time (sec) ',
 'Server Response Time (ms)',
 'Avg. Server Response Time (sec)',
 'Speed Metrics Sample ',
 'Document Interactive Time (ms) ',
 'Avg. Document Interactive Time (sec) ',
 'Document Content Loaded Time (ms)',
 'Avg. Document Content Loaded Time (sec) ',
 'DOM Latency Metrics Sample ',
 'Screen Views ',
 'Unique Screen Views ',
 'Screens / Session ',
 'Time on Screen ',
 'Avg. Time on Screen',
 'Total Events ',
 'Unique Events',
 'Event Value ',
 'Avg. Value ',
 'Sessions with Event ',
 'Events / Session with Event ',
 'Transactions ',
 'Ecommerce Conversion Rate',
 'Revenue ',
 'Avg. Order Value ',
 'Per Session Value ',
 'Shipping ',
 'Tax',
 'Total Value ',
 'Quantity',
 'Unique Purchases ',
 'Avg. Price ',
 'Product Revenue ',
 'Avg. QTY ',
 'Local Revenue ',
 'Local Shipping ',
 'Local Tax ',
 'Local Product Revenue',
 'Buy-to-Detail Rate ',
 'Cart-to-Detail Rate ',
 'Internal Promotion CTR ',
 'Internal Promotion Clicks ',
 'Internal Promotion Views ',
 'Local Product Refund Amount',
 'Local Refund Amount',
 'Product Adds To Cart ',
 'Product Checkouts',
 'Product Detail Views ',
 'Product List CTR ',
 'Product List Clicks ',
 'Product List Views ',
 'Product Refund Amount',
 'Product Refunds ',
 'Product Removes From Cart',
 'Product Revenue per Purchase ',
 'Quantity Added To Cart ',
 'Quantity Checked Out',
 'Quantity Refunded ',
 'Quantity Removed From Cart ',
 'Refund Amount',
 'Revenue per User',
 'Refunds ',
 'Transactions per User ',
 'Social Actions ',
 'Unique Social Actions ',
 'Actions Per Social Session ',
 'User Timing (ms)',
 'User Timing Sample',
 'Avg. User Timing (sec) ',
 'Exceptions',
 'Exceptions / Screen ',
 'Crashes ',
 'Crashes / Screen ',
 'Custom Metric XX Value ',
 'Calculated Metric ',
 'AdSense Revenue ',
 'AdSense Ad Units Viewed ',
 'AdSense Impressions ',
 'AdSense Ads Clicked ',
 'AdSense Page Impressions ',
 'AdSense CTR ',
 'AdSense eCPM ',
 'AdSense Exits ',
 'AdSense Viewable Impression % ',
 'AdSense Coverage ',
 'Publisher Impressions ',
 'Publisher Coverage ',
 'Publisher Monetized Pageviews',
 'Publisher Impressions / Session ',
 'Publisher Viewable Impressions % ',
 'Publisher Clicks ',
 'Publisher CTR ',
 'Publisher Revenue ',
 'Publisher Revenue / 1000 Sessions ',
 'Publisher eCPM ',
 'AdX Impressions ',
 'AdX Coverage ',
 'AdX Monetized Pageviews ',
 'AdX Impressions / Session ',
 'AdX Viewable Impressions % ',
 'AdX Clicks ',
 'AdX CTR ',
 'AdX Revenue ',
 'AdX Revenue / 1000 Sessions ',
 'AdX eCPM',
 'GAM Backfill Impressions ',
 'GAM Backfill Coverage ',
 'GAM Backfill Monetized Pageviews ',
 'GAM Backfill Impressions / Session ',
 'GAM Backfill Viewable Impressions % ',
 'GAM Backfill Clicks',
 'GAM Backfill CTR ',
 'GAM Backfill Revenue ',
 'GAM Backfill Revenue / 1000 Sessions ',
 'GAM Backfill eCPM',
 'GAM Impressions ',
 'GAM Coverage',
 'GAM Monetized Pageviews',
 'GAM Impressions / Session',
 'GAM Viewable Impressions % ',
 'GAM Clicks ',
 'GAM CTR ',
 'GAM Revenue ',
 'GAM Revenue / 1000 Sessions ',
 'GAM eCPM',
 'Users ',
 'Appviews per User',
 'Appviews Per User (LTV)',
 'Goal Completions per User ',
 'Goal Completions Per User (LTV) ',
 'Pageviews per User ',
 'Pageviews Per User (LTV) ',
 'User Retention ',
 'Revenue per User ',
 'Revenue Per User (LTV)',
 'Session Duration per User ',
 'Session Duration Per User (LTV) ',
 'Sessions per User ',
 'Sessions Per User (LTV) ',
 'Total Users',
 'Users',
 'DV360 eCPA ',
 'DV360 eCPC',
 'DV360 eCPM ',
 'DV360 CTR ',
 'DV360 Clicks ',
 'DV360 Conversions ',
 'DV360 Cost ',
 'DV360 Impressions ',
 'DV360 ROAS ',
 'SA360 CPC ',
 'SA360 CTR ',
 'SA360 Clicks ',
 'SA360 Cost ',
 'SA360 Impressions ',
 'SA360 Profit ',
 'SA360 ROAS ',
 'SA360 RPC ']
        self.metricas_codigos=['ga:users',
 'ga:newUsers',
 'ga:percentNewSessions',
 'ga:1dayUsers',
 'ga:7dayUsers',
 'ga:14dayUsers',
 'ga:30dayUsers',
 'ga:sessionsPerUser',
 'ga:sessions',
 'ga:bounces',
 'ga:bounceRate',
                               'ga:sessionDuration',
                               'ga:avgSessionDuration',
                               'ga:uniqueDimensionCombinations',
                               'ga:hits',
                               'ga:organicSearches',
                               'ga:impressions',
                               'ga:adClicks',
                               'ga:adCost',
                               'ga:CPM',
                               'ga:CPC',
                               'ga:CTR',
                               'ga:costPerTransaction',
                               'ga:costPerGoalConversion',
                               'ga:costPerConversion',
                               'ga:RPC',
                               'ga:ROAS',
                               'ga:goalXXStarts',
                               'ga:goalStartsAll',
                               'ga:goalXXCompletions',
                               'ga:goalCompletionsAll',
                               'ga:goalXXValue',
                               'ga:goalValueAll',
                               'ga:goalValuePerSession',
                               'ga:goalXXConversionRate',
                               'ga:goalConversionRateAll',
                               'ga:goalXXAbandons',
                               'ga:goalAbandonsAll',
                               'ga:goalXXAbandonRate',
                               'ga:goalAbandonRateAll',
                               'ga:pageValue',
                               'ga:entrances',
                               'ga:entranceRate',
                               'ga:pageviews',
                               'ga:pageviewsPerSession',
                               'ga:uniquePageviews',
                               'ga:timeOnPage',
                               'ga:avgTimeOnPage',
                               'ga:exits',
                               'ga:exitRate',
                               'ga:dimensionXX',
                               'ga:customVarNameXX',
                               'ga:customVarValueXX',
                               'ga:previousContentGroupXX',
                               'ga:date',
                               'ga:year',
                               'ga:month',
                               'ga:week',
                               'ga:day',
                               'ga:hour',
                               'ga:minute',
                               'ga:nthMonth',
                               'ga:nthWeek',
                               'ga:nthDay',
                               'ga:nthMinute',
                               'ga:dayOfWeek',
                               'ga:dayOfWeekName',
                               'ga:dateHour',
                               'ga:dateHourMinute',
                               'ga:yearMonth',
                               'ga:yearWeek',
                               'ga:isoWeek',
                               'ga:isoYear',
                               'ga:isoYearIsoWeek',
                               'ga:nthHour',
                               'ga:percentSearchRefinements',
                               'ga:searchDuration',
                               'ga:avgSearchDuration',
                               'ga:searchExits',
                               'ga:searchExitRate',
                               'ga:searchGoalXXConversionRate',
                               'ga:searchGoalConversionRateAll',
                               'ga:goalValueAllPerSearch',
                               'ga:pageLoadTime',
                               'ga:pageLoadSample',
                               'ga:avgPageLoadTime',
                               'ga:domainLookupTime',
                               'ga:avgDomainLookupTime',
                               'ga:pageDownloadTime',
                               'ga:avgPageDownloadTime',
                               'ga:redirectionTime',
                               'ga:avgRedirectionTime',
                               'ga:serverConnectionTime',
                               'ga:avgServerConnectionTime',
                               'ga:serverResponseTime',
                               'ga:avgServerResponseTime',
                               'ga:speedMetricsSample',
                               'ga:domInteractiveTime',
                               'ga:avgDomInteractiveTime',
                               'ga:domContentLoadedTime',
                               'ga:avgDomContentLoadedTime',
                               'ga:domLatencyMetricsSample',
                               'ga:screenviews',
                               'ga:uniqueScreenviews',
                               'ga:screenviewsPerSession',
                               'ga:timeOnScreen',
                               'ga:avgScreenviewDuration',
                               'ga:totalEvents',
                               'ga:uniqueEvents',
                               'ga:eventValue',
                               'ga:avgEventValue',
                               'ga:sessionsWithEvent',
                               'ga:eventsPerSessionWithEvent',
                               'ga:transactions',
                               'ga:transactionsPerSession',
                               'ga:transactionRevenue',
                               'ga:revenuePerTransaction',
                               'ga:transactionRevenuePerSession',
                               'ga:transactionShipping',
                               'ga:transactionTax',
                               'ga:totalValue',
                               'ga:itemQuantity',
                               'ga:uniquePurchases',
                               'ga:revenuePerItem',
                               'ga:itemRevenue',
                               'ga:itemsPerPurchase',
                               'ga:localTransactionRevenue',
                               'ga:localTransactionShipping',
                               'ga:localTransactionTax',
                               'ga:localItemRevenue',
                               'ga:buyToDetailRate',
                               'ga:cartToDetailRate',
                               'ga:internalPromotionCTR',
                               'ga:internalPromotionClicks',
                               'ga:internalPromotionViews',
                               'ga:localProductRefundAmount',
                               'ga:localRefundAmount',
                               'ga:productAddsToCart',
                               'ga:productCheckouts',
                               'ga:productDetailViews',
                               'ga:productListCTR',
                               'ga:productListClicks',
                               'ga:productListViews',
                               'ga:productRefundAmount',
                               'ga:productRefunds',
                               'ga:productRemovesFromCart',
                               'ga:productRevenuePerPurchase',
                               'ga:quantityAddedToCart',
                               'ga:quantityCheckedOut',
                               'ga:quantityRefunded',
                               'ga:quantityRemovedFromCart',
                               'ga:refundAmount',
                               'ga:revenuePerUser',
                               'ga:totalRefunds',
                               'ga:transactionsPerUser',
                               'ga:socialInteractions',
                               'ga:uniqueSocialInteractions',
                               'ga:socialInteractionsPerSession',
                               'ga:userTimingValue',
                               'ga:userTimingSample',
                               'ga:avgUserTimingValue',
                               'ga:exceptions',
                               'ga:exceptionsPerScreenview',
                               'ga:fatalExceptions',
                               'ga:fatalExceptionsPerScreenview',
                               'ga:metricXX',
                               'ga:calcMetric_<NAME>',
                               'ga:adsenseRevenue',
                               'ga:adsenseAdUnitsViewed',
                               'ga:adsenseAdsViewed',
                               'ga:adsenseAdsClicks',
                               'ga:adsensePageImpressions',
                               'ga:adsenseCTR',
                               'ga:adsenseECPM',
                               'ga:adsenseExits',
                               'ga:adsenseViewableImpressionPercent',
                               'ga:adsenseCoverage',
                               'ga:totalPublisherImpressions',
                               'ga:totalPublisherCoverage',
                               'ga:totalPublisherMonetizedPageviews',
                               'ga:totalPublisherImpressionsPerSession',
                               'ga:totalPublisherViewableImpressionsPercent',
                               'ga:totalPublisherClicks',
                               'ga:totalPublisherCTR',
                               'ga:totalPublisherRevenue',
                               'ga:totalPublisherRevenuePer1000Sessions',
                               'ga:totalPublisherECPM',
                               'ga:adxImpressions',
                               'ga:adxCoverage',
                               'ga:adxMonetizedPageviews',
                               'ga:adxImpressionsPerSession',
                               'ga:adxViewableImpressionsPercent',
                               'ga:adxClicks',
                               'ga:adxCTR',
                               'ga:adxRevenue',
                               'ga:adxRevenuePer1000Sessions',
                               'ga:adxECPM',
                               'ga:backfillImpressions',
                               'ga:backfillCoverage',
                               'ga:backfillMonetizedPageviews',
                               'ga:backfillImpressionsPerSession',
                               'ga:backfillViewableImpressionsPercent',
                               'ga:backfillClicks',
                               'ga:backfillCTR',
                               'ga:backfillRevenue',
                               'ga:backfillRevenuePer1000Sessions',
                               'ga:backfillECPM',
                               'ga:dfpImpressions',
                               'ga:dfpCoverage',
                               'ga:dfpMonetizedPageviews',
                               'ga:dfpImpressionsPerSession',
                               'ga:dfpViewableImpressionsPercent',
                               'ga:dfpClicks',
                               'ga:dfpCTR',
                               'ga:dfpRevenue',
                               'ga:dfpRevenuePer1000Sessions',
                               'ga:dfpECPM',
                               'ga:cohortActiveUsers',
                               'ga:cohortAppviewsPerUser',
                               'ga:cohortAppviewsPerUserWithLifetimeCriteria',
                               'ga:cohortGoalCompletionsPerUser',
                               'ga:cohortGoalCompletionsPerUserWithLifetimeCriteria',
                               'ga:cohortPageviewsPerUser',
                               'ga:cohortPageviewsPerUserWithLifetimeCriteria',
                               'ga:cohortRetentionRate',
                               'ga:cohortRevenuePerUser',
                               'ga:cohortRevenuePerUserWithLifetimeCriteria',
                               'ga:cohortSessionDurationPerUser',
                               'ga:cohortSessionDurationPerUserWithLifetimeCriteria',
                               'ga:cohortSessionsPerUser',
                               'ga:cohortSessionsPerUserWithLifetimeCriteria',
                               'ga:cohortTotalUsers',
                               'ga:cohortTotalUsersWithLifetimeCriteria',
                               'ga:dbmCPA',
                               'ga:dbmCPC',
                               'ga:dbmCPM',
                               'ga:dbmCTR',
                               'ga:dbmClicks',
                               'ga:dbmConversions',
                               'ga:dbmCost',
                               'ga:dbmImpressions',
                               'ga:dbmROAS',
                               'ga:dsCPC',
                               'ga:dsCTR',
                               'ga:dsClicks',
                               'ga:dsCost',
                               'ga:dsImpressions',
                               'ga:dsProfit',
                               'ga:dsReturnOnAdSpend',
                               'ga:dsRevenuePerClick']
        self.metricas_selecionadas=[]
        self.checkboxes1=[]
        self.checkboxes2=[]
        self.checkvars1 = []
        self.checkvars2 = []

        for i in self.dimensiones:
            self.checkvar1 = tk.IntVar()   # Crear variable para el Checkbutton del frame 1
            self.checkbox1 = tk.Checkbutton(self.frame1_checkbox_frame, text="{}".format(i), bg="white",
                                            fg="black", variable=self.checkvar1)  # Asociar variable al Checkbutton

            self.checkbox1.pack(anchor=tk.W)
            self.checkboxes1.append(self.checkbox1)
            self.checkvars1.append(self.checkvar1)


        for i in self.metricas:
            self.checkvar2 = tk.IntVar()  # Crear variable para el Checkbutton del frame 2
            self.checkbox2 = tk.Checkbutton(self.frame2_checkbox_frame, text="{}".format(i), bg="white",
                                            fg="black", variable=self.checkvar2)  # Asociar variable al Checkbutton
            self.checkbox2.pack(anchor=tk.W)
            self.checkvars2.append(self.checkvar2)
            self.checkboxes2.append(self.checkbox2)

        self.canvas1.create_window(0, 0, anchor=tk.NW, window=self.frame1_checkbox_frame)
        self.canvas2.create_window(0, 0, anchor=tk.NW, window=self.frame2_checkbox_frame)

        self.frame1_scrollbar = tk.Scrollbar(self.frame_izq, orient=tk.VERTICAL)
        self.frame1_scrollbar.place(x=210, height=300)
        self.frame1_scrollbar.config(command=self.canvas1.yview)
        self.canvas1.config(yscrollcommand=self.frame1_scrollbar.set)
        self.canvas1.bind("<Configure>", lambda e: self.canvas1.configure(scrollregion=self.canvas1.bbox("all")))

        self.frame2_scrollbar = tk.Scrollbar(self.frame_der, orient=tk.VERTICAL)
        self.frame2_scrollbar.place(x=210, height=300)
        self.frame2_scrollbar.config(command=self.canvas2.yview)
        self.canvas2.config(yscrollcommand=self.frame2_scrollbar.set)
        self.canvas2.bind("<Configure>", lambda e: self.canvas2.configure(scrollregion=self.canvas2.bbox("all")))

        self.boton = tk.Button(self.frame1, text="Reset", command=self.borrar_checkBOX)
        self.boton.place(x=300, y=60, width=200)

        self.boton = tk.Button(self.frame1, text="Reporte", command=self.verificar_checkbox)
        self.boton.place(x=300, y=30, width=200)



    def get_analytics_data(self, view_id, start_date, end_date, metricas, dimensiones, page_size=5000):
     """Obtiene los datos de Analytics para la vista especificada"""

     creds = Credentials.from_service_account_file('api-python-380220-366fd91b39ae.json')
     analytics = build('analyticsreporting', 'v4', credentials=creds)
     page_token = None
     data_df = []
     a = 0
     try:
      while True:
       report = analytics.reports().batchGet(
        body={
         'reportRequests': [
          {
           'viewId': view_id,
           'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
           'metrics': metricas,
           'dimensions': dimensiones,
           'pageSize': page_size,
           'pageToken': page_token
          }]
        }
       ).execute()

       for report in report.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])
        fila = []
        for row in rows:
          dimensions = row.get('dimensions', [])
          metrics = row.get('metrics', [])
          print("DIMENSIONES")
          print(dimensions)
          print("METRICAS")
          print(metrics)
          lista = metrics[0]['values']
          diccionario={}
          for i in range(len(lista)):
           diccionario[self.metricas_selecionadas[i]]=lista[i]
          for i in range(len(dimensions)):
           diccionario[self.dimensiones_seleccionadas[i]]=dimensions[i]
          data_df.append(diccionario)
          print(diccionario)
          print("-----------------------------")

       page_token = report.get('nextPageToken')
       if not page_token:
        break

      return data_df
     except Exception as e:
      print(f"An error occurred while fetching analytics data: {str(e)}")
      messagebox.showerror("Error", e)
      return None

    def filter_checkboxes_dim(self, search_query):
     for checkbox in self.checkboxes1:
      if search_query.lower() in checkbox.cget("text").lower():
       checkbox.pack(anchor=tk.W)
      else:
       checkbox.pack_forget()

    def filter_checkboxes_metricas(self, search_query):
     for checkbox in self.checkboxes2:
      if search_query.lower() in checkbox.cget("text").lower():
       checkbox.pack(anchor=tk.W)
      else:
       checkbox.pack_forget()

    def verificar_checkbox(self):
        print(self.texto_inf.get())
        print(self.texto_sup.get())
        metricas_ga=[]
        dimensiones_ga=[]

        for i in range(len(self.checkvars1)):
            if self.checkvars1[i].get() == 1:
                print("Dimension {} de frame1 marcado: {}".format(i + 1, self.dimensiones[i]))
                print("codigo: {}".format(self.dimensiones_codigos[i]))
                dimensiones_ga.append({'name': self.dimensiones_codigos[i]})
                self.dimensiones_seleccionadas.append(self.dimensiones[i])

        for i in range(len(self.checkvars2)):
            if self.checkvars2[i].get() == 1:
                print("Metrica {} de frame2 marcado: {}".format(i + 1, self.metricas[i]))
                print("codigo: {}".format(self.metricas_codigos[i]))
                metricas_ga.append({'expression': self.metricas_codigos[i]})
                self.metricas_selecionadas.append(self.metricas[i])

        print(dimensiones_ga)
        print(metricas_ga)

        df=self.get_analytics_data('242748645', self.texto_inf.get(), self.texto_sup.get(), metricas_ga, dimensiones_ga)
        print(self.metricas_selecionadas)
        print(self.dimensiones_seleccionadas)
        df_final = pd.DataFrame(df)
        df_final.to_excel("gaaaa.xlsx")
        self.dimensiones_seleccionadas = []
        self.metricas_selecionadas = []
        if df!=None:
         messagebox.showinfo("Mensaje", "Se ha cargado correctamente")

    def borrar_checkBOX(self):
        print("Hiciste clic en el botón!")
        for checkbox in self.checkboxes1:
            checkbox.deselect()

        for checkbox in self.checkboxes2:
            checkbox.deselect()



    def show_frame2(self):
        self.show_frame(self.frame2, "hi")

    def show_frame3(self):
        self.show_frame(self.frame3, "hi")

    def show_frame(self, frame, message):
        # Ocultar el marco actual
        if self.current_frame:
            self.current_frame.pack_forget()

        # Mostrar el nuevo marco y actualizar el mensaje
        self.current_frame = frame
        label = tk.Label(frame, text=message, font=("Helvetica", 18), fg="white", bg=frame["bg"])
        label.pack(fill="both", expand=True)
        frame.pack(fill="both", expand=True)

if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
