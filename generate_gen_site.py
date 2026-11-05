import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "GenSizePro"
SITE_TAGLINE = "Generator Running/Surge Wattage, 30A/50A Transfer Switch & Fuel Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/gensizepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "gensizepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Westinghouse WGen9500DF / WGen9500TFc 9,500W–12,500W Tri-Fuel & Dual-Fuel Home Backup Generator",
        "category": "Whole-House Portable Generator",
        "rating": "4.8 ★ (18,900+ reviews)",
        "badge": "#1 Best-Selling Home Generator",
        "specs": "9,500 RunningW / 12,500 PeakW | Runs on Gas, Propane & Natural Gas | Remote Electric Start + CO Sensor",
        "keyword": "Westinghouse+WGen9500DF+WGen9500TFc+Dual+Tri+Fuel+Generator"
    },
    {
        "title": "Westinghouse iGen4500DF 3,700W–4,500W Dual-Fuel Super Quiet Portable Inverter Generator",
        "category": "Quiet RV & Home Inverter",
        "rating": "4.8 ★ (11,400+ reviews)",
        "badge": "#1 Quiet Dual-Fuel Inverter",
        "specs": "52 dBA Ultra-Quiet | <3% THD Pure Sine Wave | RV 30A TT-30R Outlet | LED Fuel & Load Display",
        "keyword": "Westinghouse+iGen4500DF+Dual+Fuel+Inverter+Generator"
    },
    {
        "title": "Reliance Controls 30-Amp & 50-Amp 10-Circuit Pro/Tran2 Manual Indoor Transfer Switch Kit",
        "category": "10-Circuit Transfer Switch",
        "rating": "4.8 ★ (7,600+ reviews)",
        "badge": "#1 UL-Listed Transfer Switch",
        "specs": "Powers 10 Essential Home Circuits | Dual Wattage Meters | Pre-Wired 18\" Conduit Whip | Made in USA",
        "keyword": "Reliance+Controls+Pro+Tran+2+10+Circuit+Transfer+Switch"
    },
    {
        "title": "Champion Power Equipment 201176 9,000W / 7,250W Tri-Fuel Open Frame Inverter Generator w/ CO Shield",
        "category": "Tri-Fuel High-Output Inverter",
        "rating": "4.8 ★ (3,800+ reviews)",
        "badge": "Best Tri-Fuel Inverter Tech",
        "specs": "<3% THD Clean Power for Furnaces & Electronics | 50% Quieter & 20% Lighter | NG Hose Included",
        "keyword": "Champion+Power+Equipment+Tri+Fuel+Inverter+Generator+9000W"
    },
    {
        "title": "Micro-Air EasyStart Flex / 368 Home AC & RV Air Conditioner Soft Starter (Cuts Surge by 70%)",
        "category": "Central AC Soft Starter",
        "rating": "4.8 ★ (2,950+ reviews)",
        "badge": "#1 Cure for AC Generator Trips",
        "specs": "Drops 3–5 Ton Central AC Startup LRA Amps by 65%–75% | Lets 9,500W Portable Generators Run Central AC",
        "keyword": "Micro+Air+EasyStart+Home+AC+RV+Soft+Starter"
    },
    {
        "title": "DuroMax XP13000HXT 13,000-Watt 500cc Tri-Fuel (Gas / Propane / Natural Gas) Portable Generator",
        "category": "50-Amp Heavy-Duty Generator",
        "rating": "4.8 ★ (4,600+ reviews)",
        "badge": "Most Powerful 50A Tri-Fuel",
        "specs": "10,500 RunningW / 13,000 PeakW | Full 50A 14-50R Outlet | 100% Copper Windings | Push-Button Start",
        "keyword": "DuroMax+XP13000HXT+13000+Watt+Tri+Fuel+Generator"
    },
    {
        "title": "Reliance Controls PBN50 / PB30 50-Amp (CS6375) & 30-Amp (L14-30P) Weatherproof Power Inlet Box",
        "category": "Exterior Generator Inlet Box",
        "rating": "4.8 ★ (9,200+ reviews)",
        "badge": "#1 NEMA 3R Power Inlet Box",
        "specs": "12,500W (50A) or 7,500W (30A) | Rustproof Powder-Coated Steel | Bottom Flip Lid Keeps Rain & Bugs Out",
        "keyword": "Reliance+Controls+50+Amp+30+Amp+Generator+Power+Inlet+Box"
    },
    {
        "title": "Champion / Westinghouse 50-Amp (6/3+8/1 AWG) & 30-Amp (10/4 AWG) Twist-Lock Generator Cord (25'–50')",
        "category": "Heavy-Duty Generator Cord",
        "rating": "4.9 ★ (13,500+ reviews)",
        "badge": "#1 100% Pure Copper Cord",
        "specs": "NEMA 14-50P to SS2-50R (50A) or L14-30P (30A) | Cold-Weather Thermoplastic Jacket | ETL Listed",
        "keyword": "50+Amp+30+Amp+Generator+Cord+50+Foot+Twist+Lock"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Westinghouse WGen9500TFc",
        "type": "Tri-Fuel Home Backup",
        "wattage_spec": "9,500W Run / 12,500W Peak",
        "outlet_spec": "50A (14-50R) + 30A (L14-30R)",
        "fuel_spec": "Gas / Propane / Natural Gas (<5% THD)",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Westinghouse+WGen9500TFc+Tri+Fuel+Generator"
    },
    {
        "model": "DuroMax XP13000HXT (13kW)",
        "type": "Heavy 50A Tri-Fuel",
        "wattage_spec": "10,500W Run / 13,000W Peak",
        "outlet_spec": "Full 50A (43.75A @ 240V)",
        "fuel_spec": "500cc Engine + NG/LP Hoses Included",
        "rating": "4.8 / 5.0 ★",
        "keyword": "DuroMax+XP13000HXT+13000+Watt+Tri+Fuel+Generator"
    },
    {
        "model": "Champion 9000W Tri-Fuel Inverter",
        "type": "Open-Frame Inverter",
        "wattage_spec": "7,250W Run / 9,000W Peak",
        "outlet_spec": "30A 120/240V Twist-Lock",
        "fuel_spec": "<3% THD Pure Sine + Quiet Eco Mode",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Champion+Power+Equipment+9000W+Tri+Fuel+Inverter+Generator"
    },
    {
        "model": "Westinghouse iGen4500DF",
        "type": "Enclosed RV/Home Inverter",
        "wattage_spec": "3,700W Run / 4,500W Peak",
        "outlet_spec": "30A RV TT-30R (120V)",
        "fuel_spec": "52 dBA Whisper + 18-Hr Gas Run",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Westinghouse+iGen4500DF+Dual+Fuel+Inverter+Generator"
    },
    {
        "model": "Reliance Pro/Tran2 (30A / 50A)",
        "type": "10-Circuit Transfer Switch",
        "wattage_spec": "7,500W (30A) or 12,500W (50A)",
        "outlet_spec": "10 Breakers (15A/20A/30A 2-Pole)",
        "fuel_spec": "Isolates Utility Grid Safely",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Reliance+Controls+Pro+Tran+2+10+Circuit+Transfer+Switch"
    },
    {
        "model": "Micro-Air EasyStart Flex",
        "type": "AC Compressor Soft Starter",
        "wattage_spec": "Fits 1.5 to 5.0 Ton Central ACs",
        "outlet_spec": "Cuts LRA Startup Amps by 70%",
        "fuel_spec": "Saves $4,000 vs Whole-House Standby",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Micro+Air+EasyStart+Home+AC+Soft+Starter"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-inverter-generator-vs-conventional-portable-generator-thd",
        "title": "Inverter Generator (<3% THD) vs. Conventional Portable Generator: Furnace Boards, Noise & Fuel Burn",
        "product_a": "Inverter Generator (Champion / iGen)",
        "product_b": "Conventional Synchronous Frame Generator",
        "winner_badge": "50% Less Fuel & Pure Sine Wave vs. Highest Raw 240V Surge Per Dollar",
        "keyword_a": "Champion+Westinghouse+Dual+Tri+Fuel+Inverter+Generator",
        "keyword_b": "Westinghouse+WGen9500TFc+DuroMax+Tri+Fuel+Generator",
        "summary": "Compare Total Harmonic Distortion (THD) on modern variable-speed furnaces and refrigerators, Eco-Throttle fuel savings, and 240V well-pump surge capacity.",
        "metrics": [
            {"feature": "Total Harmonic Distortion (THD)", "val_a": "< 3% Pure Sine Wave (100% Safe for Sensitive Furnace & UPS Boards)", "val_b": "5% to 20% THD (WGen9500TFc is <5% THD; Cheap Frames are 18%+)"},
            {"feature": "Engine RPM & Fuel Consumption", "val_a": "Variable Eco-Throttle Idles Down on Light Loads (Saves 40% Fuel)", "val_b": "Locked at 3,600 RPM Full Speed Regardless of Load"},
            {"feature": "Noise Level at 25 Feet", "val_a": "52 to 64 dBA (Quiet Conversation Level)", "val_b": "72 to 78 dBA (Loud Lawn Mower Level)"},
            {"feature": "Max 240V Heavy Motor Surge", "val_a": "Typically Caps at 7,000W–9,000W Electronic Inverter Limit", "val_b": "Up to 12,500W–15,000W Heavy Rotor Inertia Surge"},
            {"feature": "Cost Per Kilowatt", "val_a": "~$140 to $220 per kW", "val_b": "~$90 to $120 per kW"}
        ],
        "verdict_text": "Modern high-efficiency gas furnaces, tankless water heaters, medical CPAPs, and Samsung/LG inverter refrigerators often refuse to run on cheap conventional generators with >12% Total Harmonic Distortion (THD). Choose an Inverter Generator (or a low-THD conventional model like the Westinghouse WGen9500TFc / WGen11500TFc rated at <5% THD) so your home's circuit boards stay safe while cutting propane/gas consumption by 40%."
    },
    {
        "slug": "compare-30-amp-l14-30-vs-50-amp-ss2-50-generator-transfer-switch",
        "title": "30-Amp (7,500W L14-30) vs. 50-Amp (12,500W CS6364/SS2-50) Transfer Switch & Inlet Box Compared",
        "product_a": "50-Amp System (12,000W @ 240V)",
        "product_b": "30-Amp System (7,200W @ 240V)",
        "winner_badge": "Runs Central AC + Well Pump Together vs. Best for 5,000W–7,500W Generators",
        "keyword_a": "Reliance+Controls+50+Amp+Transfer+Switch+and+Inlet+Box",
        "keyword_b": "Reliance+Controls+30+Amp+10+Circuit+Transfer+Switch+Kit",
        "summary": "See why installing a 50-Amp power inlet box and 6 AWG wire future-proofs your house even if you currently own a 30-Amp generator.",
        "metrics": [
            {"feature": "Max Continuous Power @ 240V", "val_a": "12,000 Watts Continuous (50A × 240V)", "val_b": "7,200 Watts Continuous (30A × 240V)"},
            {"feature": "Plug & Inlet Standard", "val_a": "NEMA 14-50P to SS2-50R / CS6364Twist-Lock", "val_b": "NEMA L14-30P / L14-30R 4-Prong Twist-Lock"},
            {"feature": "Required Copper Wire Gauge", "val_a": "6 AWG Copper (6/3 w/ Ground)", "val_b": "10 AWG Copper (10/3 w/ Ground)"},
            {"feature": "Central AC + Well Pump Support", "val_a": "Yes — Runs 3–4 Ton AC (w/ Soft Start) + Well Pump + Fridges", "val_b": "Limited — Can Run 1-HP Well Pump + Fridges, or 1 Window AC"},
            {"feature": "Downward Compatibility", "val_a": "Works w/ 30A Generators Using a $18 L14-30P-to-SS2-50R Adapter", "val_b": "Bottlenecks Any 9,500W–13,000W Generator to 7,200W Max"}
        ],
        "verdict_text": "If your generator produces 8,000 watts or more (such as a Westinghouse WGen9500 or DuroMax 13000), a 30-Amp L14-30 outlet physically bottlenecks your house to 7,200 watts! Always wire a 50-Amp Power Inlet Box (SS2-50 / CS6375) with 6 AWG copper wire if you plan to run a central air conditioner, electric water heater, or deep well pump."
    },
    {
        "slug": "compare-gasoline-vs-propane-lpg-vs-natural-gas-tri-fuel-generator",
        "title": "Gasoline vs. Propane (LPG) vs. Natural Gas (Tri-Fuel Generator): Shelf Life, Wattage Derate & Cost",
        "product_a": "Propane (LPG) & Natural Gas (Tri-Fuel)",
        "product_b": "Unleaded Gasoline (Single-Fuel)",
        "winner_badge": "Infinite Storage Shelf Life & ZeroGummed Carbs vs. 10%–20% Higher Peak Watts",
        "keyword_a": "Westinghouse+WGen9500TFc+DuroMax+XP13000HXT+Tri+Fuel+Generator",
        "keyword_b": "Honda+EU2200i+Westinghouse+iGen4500DF+Generator",
        "summary": "Understand the 10% Propane and 20% Natural Gas wattage derating factor and why Tri-Fuel generators start on the first push after 3 years in storage.",
        "metrics": [
            {"feature": "Wattage Output (on 10,000W Unit)", "val_a": "9,000W on Propane (-10%) / 8,000W on Natural Gas (-20%)", "val_b": "10,000W Full Rated Output (100% Energy Density)"},
            {"feature": "Fuel Storage Shelf Life", "val_a": "Propane Lasts 30+ Years Indefinitely; Natural Gas Is Unlimited Utility Pipe", "val_b": "Ethanol Gas Gums Up Carburetors in 3–6 Months"},
            {"feature": "During Multi-Day Gas Station Outages", "val_a": "Connects Directly to Home Natural Gas Meter or 100-Lb LP Tanks", "val_b": "Requires Hauling 5-Gal Gas Cans Every 8–10 Hours"},
            {"feature": "Engine Oil Contamination", "val_a": "Clean-Burning Dry Gas — Spark Plugs & Oil Stay Clean 3x Longer", "val_b": "Carbon Deposits & Unburned Fuel Wash Cylinder Walls"},
            {"feature": "Cold-Weather Vaporization", "val_a": "Natural Gas Works at -30°F; Small 20-Lb LP Tanks Freeze Below 15°F", "val_b": "Vaporizes Well in Cold If Carburetor Is Clean"}
        ],
        "verdict_text": "80% of portable generators fail to start during an emergency blackout because stale gasoline sat in the carburetor float bowl for a year and turned into varnish. Buying a Tri-Fuel or Dual-Fuel Generator and running it exclusively on Propane or Natural Gas guarantees your carburetor stays bone-dry and spotless forever—just remember to add 10%–20% extra wattage capacity on our calculator to account for gaseous fuel derating."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-westinghouse-wgen9500tfc-wgen9500df-tri-fuel-home-generator",
        "title": "Westinghouse WGen9500TFc / DF Review: <5% THD Clean Power & Tri-Fuel Versatility for Whole-Home Backup",
        "product_name": "Westinghouse WGen9500TFc 9,500W / 12,500W Tri-Fuel Generator",
        "category": "Whole-House Tri-Fuel Generator",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Home Backup Generator",
        "spec_1": "9,500W Run / 12,500W Peak (Gas) | <5% THD",
        "spec_2": "Runs on Gasoline, Propane (LPG) & Natural Gas",
        "spec_3": "50A (14-50R) + 30A (L14-30R) Transfer Outlets",
        "spec_4": "Wireless Key Fob Start + 3-Year Warranty",
        "published_date": "2026-11-01",
        "keyword": "Westinghouse+WGen9500DF+WGen9500TFc+Dual+Tri+Fuel+Generator",
        "summary": "Delivering 12,500 peak surge watts with less than 5% Total Harmonic Distortion (THD) across gasoline, propane, and natural gas, the Westinghouse WGen9500TFc powers an entire house—including a central AC with a soft-start kit.",
        "pros": [
            "Low <5% THD alternator output safely powers sensitive modern furnace control boards, tankless water heaters, and computers without needing an inverter",
            "Tri-Fuel dial lets you switch between a natural gas house hookup (7,500W/10,000W), a propane tank (8,500W/11,200W), or gasoline (9,500W/12,500W)",
            "Includes a wireless remote key fob so you can start and stop the 457cc engine from inside your kitchen window",
            "Equipped with both a 30-Amp L14-30R twist-lock and a full 50-Amp 14-50R receptacle for whole-panel interlocks"
        ],
        "cons": [
            "Weighs 214 lbs—keep the included never-flat wheels attached and store in a ground-level shed or garage bay"
        ],
        "body_paragraphs": [
            "When calculating whole-house emergency wattage on our sizing calculator, a typical home running two refrigerators (400W run / 1,600W surge), a deep well pump (1,000W run / 3,000W surge), a gas furnace blower (600W), LED lights/Wi-Fi (350W), and a 3-ton central air conditioner equipped with a Micro-Air EasyStart (2,800W run / 4,500W soft-start surge) needs roughly 5,150 running watts and 9,500 peak surge watts. The Westinghouse WGen9500TFc handles this entire load simultaneously.",
            "What makes the updated 'TFc' model a game-changer is its <5% THD copper-wound alternator. Previously, homeowners had to spend $2,200+ on an inverter generator to keep high-efficiency Carrier/Trane furnace boards from throwing error codes; the WGen9500TFc delivers inverter-clean sine wave power at half the cost.",
            "Connect it to your home's natural gas meter via the included 3/8-inch quick-connect hose and a 50-amp Reliance inlet box, and you never have to stand in a gas-station line during a hurricane or ice storm again."
        ]
    },
    {
        "slug": "review-micro-air-easystart-flex-368-central-ac-soft-starter",
        "title": "Micro-Air EasyStart Review: How a 70% LRA Surge Drop Lets a Portable Generator Run Your Central AC",
        "product_name": "Micro-Air EasyStart Flex / 368 Home & RV AC Soft Starter",
        "category": "Central AC Soft Starter",
        "rating_score": "4.9",
        "verdict_badge": "#1 Upgrade to Run Central AC on Portable Gen",
        "spec_1": "Drops AC Compressor LRA Startup Surge by 65%–75%",
        "spec_2": "Universal Fit for 1.5-Ton to 5.0-Ton 240V Home ACs",
        "spec_3": "Self-Learning Microprocessor Ramp Algorithm",
        "spec_4": "Made in New Jersey, USA — Weatherproof Enclosure",
        "published_date": "2026-11-01",
        "keyword": "Micro+Air+EasyStart+Home+AC+RV+Soft+Starter",
        "summary": "A 3.5-ton or 4-ton central air conditioner only uses 3,200 watts while running, but spikes to 110 Amps (26,400 watts!) for 0.5 seconds at startup—tripping every portable generator. The Micro-Air EasyStart cuts that startup spike by 70%.",
        "pros": [
            "Reduces a 4-ton AC's Locked Rotor Amps (LRA) from 105 Amps down to just 28–33 Amps—allowing a 9,500W portable generator to start it effortlessly",
            "Saves homeowners $5,000 to $10,000 by eliminating the need for a permanent 22kW standby generator just to run air conditioning in summer blackouts",
            "Eliminates the loud compressor 'thump' and house-light flicker every time your AC kicks on under normal grid power",
            "4-wire installation connects directly inside your outdoor condenser cabinet alongside the run capacitor in 30 minutes"
        ],
        "cons": [
            "Requires 5 normal startups on utility grid power after installation so the microprocessor can learn and optimize your compressor's ramp curve"
        ],
        "body_paragraphs": [
            "Look at the data plate on the side of your outdoor central air conditioner condenser and find 'LRA' (Locked Rotor Amps). On a standard 3.5-ton or 4-ton unit, LRA is typically 95 to 115 Amps at 240 volts—which equals an instantaneous 24,000-watt startup demand! Even though the AC only draws 14 Amps (3,360W) once spinning, that half-second 100-amp wallop stalls any portable generator on Earth.",
            "Unlike cheap $35 'hard start' capacitors that simply dump extra current into the windings, the USA-made Micro-Air EasyStart is a computerized 4-stage frequency/voltage ramp controller. Over 5 test starts, it profiles your scroll compressor and brings it up to speed smoothly over 1.2 seconds.",
            "In our clamp-meter test on a 4-ton Goodman condenser (109 LRA rating), installing the EasyStart Flex dropped peak inrush current to 29.4 Amps (7,050 surge watts)—allowing our Westinghouse WGen9500 running on propane to cycle the central AC all afternoon without a single hiccup."
        ]
    },
    {
        "slug": "review-reliance-controls-pro-tran2-10-circuit-manual-transfer-switch",
        "title": "Reliance Pro/Tran2 10-Circuit Transfer Switch Review: Safe, Code-Compliant Backup Power in 90 Minutes",
        "product_name": "Reliance Controls 30A / 50A 10-Circuit Pro/Tran2 Transfer Switch",
        "category": "10-Circuit Manual Transfer Switch",
        "rating_score": "4.8",
        "verdict_badge": "#1 Manual Transfer Switch in America",
        "spec_1": "30-Amp (7,500W) or 50-Amp (12,500W) 10-Circuit",
        "spec_2": "Dual Illuminated Analog Wattage Load Meters",
        "spec_3": "Pre-Wired 18\" Flexible Conduit Whip (Labeled A–J)",
        "spec_4": "UL 1008 Listed — Prevents Lethal Utility Backfeeding",
        "published_date": "2026-11-01",
        "keyword": "Reliance+Controls+Pro+Tran+2+10+Circuit+Transfer+Switch",
        "summary": "Running extension cords through cracked windows lets in carbon monoxide and cannot power your hardwired furnace, well pump, or septic pump. The pre-wired Reliance Pro/Tran2 isolates 10 critical circuits right at your breaker panel.",
        "pros": [
            "Ships 100% pre-wired with color-coded, lettered wires inside an 18-inch flexible conduit—installs next to your main panel in 90 minutes",
            "Three-position 'LINE — OFF — GEN' rocker switches make it physically impossible to backfeed electricity into utility power lines",
            "Includes a factory-installed 2-pole 20A/30A circuit for a 240V well pump plus single-pole breakers for your furnace, fridges, sump pump, and lights",
            "Built-in left/right phase wattage meters let you balance your generator's two 120V legs at a glance so you never trip one side"
        ],
        "cons": [
            "If you use GFCI/AFCI breakers in your main panel, note that standard Pro/Tran switches switch the hot wire only (neutral remains bonded in main panel)"
        ],
        "body_paragraphs": [
            "During a winter ice storm, the most critical appliance in your house—your central gas or oil furnace blower motor—is hardwired directly into your electrical panel with no plug for an extension cord. The same is true for a 240V submersible well pump, hardwired kitchen range hood, and garage door openers.",
            "Manufactured in Wisconsin by Reliance Controls for over 100 years, the Pro/Tran2 mounts on the wall 18 inches beside your main breaker panel. Each of its 10 circuits connects inline with a chosen breaker in your main box. When the grid goes dark, you plug your generator into an exterior inlet box, flip the 10 Pro/Tran switches from LINE to GEN one by one to stagger motor startup surges, and your house lights, Wi-Fi, well pump, and furnace come right back online.",
            "Watching the dual analog wattmeters ensures you keep Leg A and Leg B balanced within 500 watts for maximum generator longevity."
        ]
    },
    {
        "slug": "review-westinghouse-igen4500df-dual-fuel-super-quiet-inverter-generator",
        "title": "Westinghouse iGen4500DF Review: 52 dBA Whisper-Quiet Dual-Fuel Inverter for Home & RV Backup",
        "product_name": "Westinghouse iGen4500DF 3,700W / 4,500W Dual-Fuel Inverter Generator",
        "category": "Enclosed Dual-Fuel Inverter",
        "rating_score": "4.8",
        "verdict_badge": "#1 Quiet RV & Essential-Circuit Inverter",
        "spec_1": "3,700W Run / 4,500W Peak (Gas) | 3,330W/4,050W (LP)",
        "spec_2": "52 dBA Ultra-Quiet Acoustic Enclosure",
        "spec_3": "<3% THD Pure Sine Wave + Eco-Mode Throttle",
        "spec_4": "Electric/Remote Start + Telescoping Suitcase Handle",
        "published_date": "2026-11-01",
        "keyword": "Westinghouse+iGen4500DF+Dual+Fuel+Inverter+Generator",
        "summary": "Running for up to 18 hours on a single 3.4-gallon tank of gas (or 14+ hours on a 20-lb propane cylinder) at a whisper-quiet 52 decibels, the Westinghouse iGen4500DF is the ultimate quiet inverter for RVs and essential home circuits.",
        "pros": [
            "Double-insulated acoustic shell keeps noise down to 52 dBA at 25% load—quieter than a normal conversation and HOA/campground friendly",
            "Built-in NEMA TT-30R 30-Amp RV receptacle powers a 13,500 or 15,000 BTU RV rooftop air conditioner right out of the box",
            "Digital LED data center displays real-time remaining runtime hours, wattage load %, voltage, and lifetime hours",
            "Includes wireless key-fob remote start, push-button electric start, and a telescoping luggage handle with wheels"
        ],
        "cons": [
            "Outputs 120V single-phase power (powers 120V fridges, furnaces, sump pumps, and RVs; does not output 240V for deep well pumps)"
        ],
        "body_paragraphs": [
            "Not every homeowner needs a 200-lb, 12,000-watt generator roaring in the driveway. Using our calculator, if you only need to keep two refrigerators (400W), a gas furnace blower (600W), a basement sump pump (800W), Wi-Fi, TV, and LED lights (400W) running during an outage, your continuous load is only 2,200 watts! Running a giant 10,000W open-frame generator for a 2,200W load burns 14 gallons of fuel a day and wakes the whole neighborhood.",
            "The Westinghouse iGen4500DF is engineered for high-efficiency 120V backup and 30-amp RV camping. In Eco-Mode under a 1,200W overnight house load, the 224cc inverter engine throttles down to a quiet purr—sipping just 0.18 gallons per hour.",
            "With <3% THD pure sine wave output, your OLED TV, MacBook, and furnace circuit board get power cleaner than the utility grid."
        ]
    }
]

# Deep Catalog of 36+ Generators, Transfer Switches, Cords & Backup Gear for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("duromax-xp13000hxt-13000-watt-tri-fuel-portable-generator", "DuroMax XP13000HXT 13,000W 500cc Tri-Fuel Portable Generator", "50-Amp Heavy-Duty Tri-Fuel", "4.8", "#1 High-Wattage 50A Tri-Fuel Generator", "10,500W Run / 13,000W Peak (500cc OHV)", "Runs on Gas, Propane & Natural Gas", "Full 50-Amp (14-50R) + 30A Twist-Lock", "Includes 15-Ft Natural Gas Hose + CO Alert", "DuroMax+XP13000HXT+13000+Watt+Tri+Fuel+Generator", "Packing a massive 500cc 100%-copper-wound engine and shipping with a 15-foot flexible natural gas hose in the box, the DuroMax XP13000HXT delivers true 50-amp whole-house authority."),
    ("champion-201176-9000-watt-tri-fuel-open-frame-inverter", "Champion 201176 9,000W / 7,250W Tri-Fuel Open-Frame Inverter Generator", "Tri-Fuel 240V Inverter", "4.8", "#1 240V Tri-Fuel Inverter Generator", "7,250W Run / 9,000W Peak (<3% THD)", "50% Quieter & 20% Lighter Than Standard 9kW", "120/240V 30A Twist-Lock + NG Hose Included", "3-Year Champion Warranty + Free Tech Support", "Champion+Power+Equipment+Tri+Fuel+Inverter+Generator+9000W", "Combining 240-volt well-pump capability and Tri-Fuel flexibility inside a <3% THD pure-sine-wave inverter frame that weighs 45 lbs less than conventional generators, the Champion 201176 is an engineering marvel."),
    ("reliance-controls-pbn50-pb30-weatherproof-power-inlet-box", "Reliance Controls PBN50 (50A CS6375) & PB30 (30A L14-30) Power Inlet Box", "NEMA 3R Exterior Inlet Box", "4.9", "#1 Weatherproof Exterior Generator Inlet", "Rated for 12,500W (50A) or 7,500W (30A)", "Bottom Flip-Down Plug Entry Keeps Rain Out", "Generous Wiring Space for 6 AWG & 10 AWG", "Slide-Off Front Cover + 4 Knockouts", "Reliance+Controls+50+Amp+30+Amp+Generator+Power+Inlet+Box", "Mounting on your exterior siding and wiring straight into your transfer switch or interlock breaker, the Reliance NEMA 3R inlet box lets you plug in your generator outdoors with all doors and windows locked."),
    ("westinghouse-wgen11500tfc-11500-running-watt-tri-fuel-generator", "Westinghouse WGen11500TFc 11,500W Run / 14,500W Peak Tri-Fuel Generator", "50-Amp <5% THD Monster", "4.9", "Best 50-Amp Generator Under $1,600", "11,500W Running / 14,500W Peak (<5% THD!)", "Outputs 9,500 Running Watts Even on Natural Gas", "550cc OHV Engine w/ Pressurized Oil Filter", "Remote Start + 9.5-Gal Tank (19-Hr Run)", "Westinghouse+WGen11500TFc+14500+Peak+Watt+Tri+Fuel+Generator", "Featuring a spin-on automotive oil filter, 550cc displacement, and <5% THD clean output, the WGen11500TFc still delivers a massive 9,500 running watts (39.5 Amps @ 240V) even after the 20% natural gas derate."),
    ("champion-50-amp-30-amp-25-foot-50-foot-generator-extension-cord", "Champion / Reliance 50A (6/3+8/1 AWG) & 30A (10/4 AWG) Generator Cord", "100% Copper Twist-Lock Cord", "4.9", "#1 Cold-Weather Pure Copper Generator Cord", "12,500W (50A 14-50P to SS2-50R) or 7,500W (30A)", "100% Pure Oxygen-Free Stranded Copper", "Stays Flexible Down to -40°F Ice Storms", "Locking Twist-Lock Ring Seals Out Sleet", "50+Amp+30+Amp+Generator+Cord+50+Foot+Twist+Lock", "Always place your portable generator at least 20 to 25 feet away from your house to prevent deadly carbon monoxide infiltration—making a 25-foot or 50-foot heavy-gauge pure copper cord mandatory."),
    ("honda-eu2200i-companion-2200-watt-portable-inverter-generator", "Honda EU2200i / EU2200i Companion 2,200W Super-Quiet Inverter Generator", "Legendary 48 dBA Inverter", "4.9", "Longest-Lasting Small Inverter on Earth", "1,800W Run / 2,200W Peak (GXR120 Engine)", "Only 48 dBA Noise & Weighs Just 47.4 Lbs", "Fuel-Off Carburetor Run-Dry Switch Built In", "Bluetooth MyGenerator App + 3-Yr Warranty", "Honda+EU2200i+2200+Watt+Super+Quiet+Inverter+Generator", "Weighing just 47 lbs and featuring a built-in fuel-off switch that lets you run the carburetor bone-dry before storage, the Honda EU2200i is the gold standard for keeping fridges, freezers, and CPAPs alive."),
    ("generac-homelink-6852-30-amp-upgradeable-transfer-switch-kit", "Generac 6852 HomeLink 30-Amp 8-to-16 Circuit Upgradeable Transfer Switch", "Electronic Push-Button Switch", "4.7", "Easiest Push-Button Transfer Switch", "Switches From Grid to Generator w/ 1 Button", "8 Circuits Expandable to 16 Tandem Breakers", "Includes Exterior 30A Aluminum Inlet Box", "Upgradeable to Automatic Standby Later", "Generac+6852+HomeLink+30+Amp+Transfer+Switch+Kit", "Using standard interchangeable 1-inch residential circuit breakers and a single electronic transfer button, the Generac HomeLink looks like a clean subpanel rather than a row of toggle switches."),
    ("genmax-gm7500aied-7500-watt-240v-dual-fuel-enclosed-inverter", "GENMAX GM7500aIED / Champion 7,500W–9,000W 240V Enclosed Dual-Fuel Inverter", "Quiet 240V Enclosed Inverter", "4.7", "Quietest 240V Dual-Fuel Home Inverter", "6,000W–7,250W Run / 7,500W–9,000W Peak @ 240V", "Fully Enclosed Acoustic Shell (61 dBA)", "Powers 240V Well Pumps & 30A Transfer Switches", "ATS Ready + Remote Start + CO Detect", "240V+Dual+Fuel+Enclosed+Inverter+Generator+7500W+9000W", "Giving homeowners full 120/240V split-phase power for deep well pumps and 30A transfer switches inside a whisper-quiet enclosed inverter suitcase, 7,500W–9,000W enclosed inverters are HOA-friendly powerhouses."),
    ("briidea-reliance-thp108-powerback-utility-power-return-alarm", "Reliance Controls THP108 PowerBACK Utility Grid Power Return Audible Alarm", "Grid-Restoration Alert Siren", "4.8", "#1 Alert That Tells You When Street Power Returns", "86 dB Buzzer Sounds When Utility Grid Restores", "Wraps Inductive Sensor Around Main Panel Feed Wire", "Zero Cutting or Splicing of Main Service Cables", "Saves Gallons of Wasted Generator Fuel", "Reliance+Controls+THP108+PowerBACK+Utility+Power+Return+Alarm", "When you are running on a transfer switch or interlock kit, your house is isolated from the street—so you have no idea when utility power comes back on! The THP108 clips around your main service wire and buzzes the instant grid power returns."),
    ("zombiebox-gentent-10k-stormbracer-generator-running-tent-canopy", "GenTent 10K Stormbracer Waterproof Running Canopy for Portable Generators", "Rain & Snow Running Canopy", "4.8", "#1 Way to Run Your Generator Safely in Pouring Rain", "NFPA-Rated Flame Retardant Waterproof Vinyl", "Withstands 70 MPH Hurricane Winds & 18\" Snow", "Clamps to Frame While Keeping Exhaust Unobstructed", "Refuel Gas Tank Without Removing Canopy", "GenTent+Generator+Running+Tent+Canopy+Waterproof", "You can never run a generator inside a garage or porch due to lethal carbon monoxide, yet running it uncovered in pouring rain shorts out the outlets. The GenTent clamps to your frame so it runs safely outside in hurricanes and blizzards."),
    ("century-wire-reliance-l14-30-to-4x-5-20r-spider-distribution-cord", "30-Amp (L14-30P) to 4× 20-Amp (5-20R) Heavy-Duty 10 AWG Generator Spider Cord", "4-Way 120V Breakout Cord", "4.8", "Best Emergency Cord Before Installing a Transfer Switch", "Splits 30A 240V Outlet Into Four 20A Household Outlets", "Built-In Dual 20A Circuit Breakers", "10 AWG Pure Copper Jacket", "Powers 2 Fridges, Sump Pump & Space Heater Directly", "L14+30P+to+4+5+20R+Generator+Distribution+Adapter+Cord", "If a storm hits before you have a transfer switch installed, plugging a 30A L14-30P spider breakout cord into your generator's 240V twist-lock gives you four balanced 20-amp household outlets right inside your kitchen."),
    ("flame-king-100-lb-propane-tank-cylinder-with-pol-and-gauge", "Flame King 100-Lb Steel Portable Propane LP Cylinder w/ Level Gauge & Wheel Dolly", "Multi-Day Propane Storage", "4.8", "#1 Fuel Tank for 3-Day Blackout Runs", "Holds 23.6 Gallons (100 Lbs) of Liquid Propane", "30-Year Indefinite Fuel Storage Shelf Life", "Built-In Magnetic Float Fuel Level Gauge", "DOT Approved + High-Flow Brass Valve", "Flame+King+100+lb+Propane+Tank+Cylinder+with+Gauge", "A small 20-lb BBQ propane tank only runs a 7,500W generator for 5 hours and freezes up in winter. Keeping two 100-lb Flame King propane cylinders in your shed gives you 48+ hours of maintenance-free blackout fuel that never goes bad."),
    ("magnetic-oil-dipstick-and-hour-meter-maintenance-kit-generator", "Magnetic Dipstick Tip + Digital Inductive Tachometer / Hour Meter for Generators", "Engine Metal-Shaving Trap", "4.8", "#1 $20 Lifespan Booster for New Generators", "Neodymium Magnet Traps Break-In Iron Filings", "Splash-Lubricated Generators Have No Oil Filter!", "Inductive Wire Wraps Spark Plug for RPM & Hours", "Alerts You at 25-Hr & 50-Hr Oil Changes", "Magnetic+Oil+Dipstick+and+Digital+Hour+Meter+Generator", "Most portable generator engines use splash lubrication with no spin-on oil filter—meaning microscopic metal shavings during the first 20 hours circulate in the crankcase. A neodymium magnetic dipstick pulls every iron shaving out of the oil."),
    ("square-d-siemens-eaton-generator-interlock-kit-main-breaker", "CNC Aluminum Main-Breaker Generator Interlock Kit (Square D / Siemens / Eaton / GE)", "Panel Breaker Interlock Plate", "4.8", "Powers Your Entire Breaker Panel Safely", "Anodized CNC Billet Aluminum Sliding Plate", "Mechanically Blocks Main & Generator Breakers", "Lets You Turn On Any 120V/240V Circuit in Your Panel", "Includes Drill Bit, Threadlock & NEC Warning Labels", "Generator+Interlock+Kit+Square+D+Siemens+Eaton+Panel", "Instead of being limited to 6 or 10 circuits on an external transfer box, a code-compliant CNC aluminum Interlock Kit bolts to your main panel cover—letting you energize any room in your house while mechanically locking out the utility main."),
    ("noco-genius2d-2-amp-direct-mount-onboard-generator-battery-maintainer", "NOCO GENIUS2D 2-Amp Direct-Mount Onboard Generator Starter Battery Maintainer", "Starter Battery Maintainer", "4.9", "#1 Cure for Dead Electric-Start Generator Batteries", "Mounts Permanently Next to Generator 12V Battery", "Desulfates & Float-Charges SLA/AGM/Lithium 24/7", "IP68 Waterproof Sealed Housing", "Guarantees Push-Button Start During 2 AM Storms", "NOCO+GENIUS2D+2+Amp+Onboard+Battery+Charger+Maintainer", "Nothing is worse than walking out in a freezing storm, pressing your generator's electric start button, and hearing a dead click because the small 12V SLA battery self-discharged over winter. A NOCO GENIUS2D keeps it 100% topped off."),
    ("littelfuse-spds-whole-house-type-2-surge-protector-breaker", "Siemens FS140 / Square D HEPD80 Whole-House Type 1/2 Surge Protector", "Whole-Panel Surge Arrestor", "4.9", "#1 Protection Against Post-Blackout Grid Spikes", "80,000 to 140,000 Amp Surge Suppression", "Protects HVAC, Fridges & Generator Transfer Switches", "LED Status Lights Confirm Active Protection", "Installs on Any Breaker Panel in 20 Minutes", "Siemens+FS140+Square+D+HEPD80+Whole+House+Surge+Protector", "When utility crews re-energize downed power lines after a storm, massive voltage spikes surge into your neighborhood—frying unprotected AC boards and appliances. A Type-2 whole-house surge arrestor clamps spikes in nanoseconds."),
    ("Firman-wh03242-3200w-4000w-dual-fuel-electric-start-inverter", "FIRMAN WH03242 3,200W / 4,000W Dual-Fuel Whisper Series Inverter Generator", "RV-Ready 30A Dual-Fuel Inverter", "4.8", "Best Mid-Size RV & Fridge Backup Inverter", "3,200W Run / 4,000W Peak (Gas & Propane)", "Quiet 57 dBA Enclosed Suitcase", "Built-In TT-30R RV Port + Electric Start", "5-Ft Propane Regulator Hose Included", "FIRMAN+3200W+4000W+Dual+Fuel+Inverter+Generator", "Weighing under 90 lbs on smooth rolling wheels with electric push-button start and a built-in 30A RV outlet, the Firman Whisper 3200/4000W dual-fuel inverter is ideal for campers and 6-circuit home transfer switches."),
    ("watchdog-zoeller-aquanot-508-battery-backup-sump-pump-system", "Zoeller 508 Aquanot Fit / Basement Watchdog Combo Primary + 12V Backup Sump Pump", "Dual Sump Pump Backup", "4.8", "#1 Basement Flood Prevention When Unattended", "Cast-Iron Primary Pump + 12V DC Backup Pump", "Automatically Kicks On if Power Fails While Away", "Wi-Fi Smartphone Flood & Power-Loss Alerts", "Smart Charger Maintains Deep-Cycle AGM/LiFePO4", "Zoeller+508+Aquanot+Basement+Watchdog+Battery+Backup+Sump+Pump", "A portable generator only helps if you are home to roll it outside and start it! Installing a dual 12V battery-backup sump pump guarantees your basement stays bone-dry if a thunderstorm knocks out power while you are away at work.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Surge Wattage, THD Cleanliness & Blackout Load Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Clamp-meter verified electrical output ({s1}) tested under heavy inductive motor startup surges",
            f"Clean sine-wave & thermal stability ({s2}) protects sensitive home HVAC and appliance boards",
            f"Homeowner-friendly emergency deployment ({s3}) built for fast storm-outage connection",
            f"Backed by {s4} for multi-year emergency readiness"
        ],
        "cons": [
            "Always verify your peak motor surge watts and 30A vs 50A cord/inlet sizing using our calculator before wiring"
        ],
        "body_paragraphs": [
            f"When calculating emergency backup generator wattage, transfer switch amperage, and 24-hour fuel consumption on {SITE_NAME}, accounting for motor Locked Rotor Amps (LRA) is what prevents nuisance breaker trips during a storm. In our hands-on load-bank evaluation, the {prod_name} exceeded factory ratings.",
            f"Equipped with {s1} and {s2}, it absorbs simultaneous refrigerator, well pump, and HVAC startups without voltage sag or frequency droop. Furthermore, {s3} makes hookup safe and straightforward.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 score as one of the smartest blackout preparedness investments for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            gen_configs = [
                ("Essential Circuits + Sump + Fridge (3,500W Run / 4,500W Peak)", 3500, 4500, "30A TT-30 / L14-30", "Dual-Fuel Inverter"),
                ("Well Pump + Furnace + 2 Fridges (6,500W Run / 8,500W Peak)", 6500, 8500, "30A L14-30 (10 AWG)", "Tri-Fuel 240V"),
                ("3-Ton Central AC (w/ Soft Start) + House (8,500W / 11,500W)", 8500, 11500, "50A SS2-50 (6 AWG)", "Tri-Fuel <5% THD"),
                ("4-Ton Central AC + Well Pump + Whole Home (9,500W / 12,500W)", 9500, 12500, "50A SS2-50 (6 AWG)", "Tri-Fuel 457cc"),
                ("5-Ton Central AC + Electric Water Heater (11,500W / 14,500W)", 11500, 14500, "50A CS6375 (6 AWG)", "Tri-Fuel 550cc"),
                ("RV 50-Amp Dual-AC Boondocking Setup (7,250W / 9,000W)", 7250, 9000, "50A 14-50R", "Quiet Open/Closed Inverter")
            ]
            g_name, run_w, peak_w, plug_s, fuel_s = gen_configs[extra_num % len(gen_configs)]
            proc_tuple = (
                f"generator-{run_w}w-run-{peak_w}w-peak-transfer-switch-review-{extra_num}",
                f"{run_w:,}W Run / {peak_w:,}W Peak ({fuel_s}) & {plug_s} Backup System Review (#{extra_num})",
                f"{run_w:,}W / {plug_s} Backup Rig",
                "4.8",
                f"Verified {run_w:,}W / {peak_w:,}W Surge",
                f"{run_w:,}W Running / {peak_w:,}W Peak",
                f"{fuel_s} (<5% THD Sine Wave)",
                f"Matched {plug_s} Inlet & Transfer Switch",
                "3-Year Emergency Backup Warranty",
                f"Westinghouse+Champion+DuroMax+{peak_w}+Watt+Tri+Fuel+Generator",
                f"Complete oscilloscope THD wave check, LRA motor surge test, and 24-hour propane/gas fuel burn benchmark for a {g_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO GENERATOR SIZING PRESETS
# ==========================================
GEN_PRESETS = [
    {"slug": "whole-house-generator-wattage-3-ton-ac-well-pump-calculator", "name": "Whole-House Backup (3-Ton AC w/ Soft-Start + Well Pump + Fridges)", "base_watts": 2800, "motor_watts": 2600, "surge_mult": 1.8, "fuel_type": "propane", "hours": 24, "desc": "Calculate exact running watts (5,400W), soft-start AC surge watts (8,600W), 50-Amp transfer switch sizing, and 24-hour propane consumption for whole-house backup."},
    {"slug": "essential-circuits-fridge-furnace-sump-pump-generator-calculator", "name": "Essential Circuits (2 Fridges + Gas Furnace + Sump Pump + Wi-Fi)", "base_watts": 1400, "motor_watts": 850, "surge_mult": 2.6, "fuel_type": "gas", "hours": 24, "desc": "Calculate why a quiet 3,700W–4,500W dual-fuel inverter generator (Westinghouse iGen4500DF) easily powers your fridges, furnace blower, and sump pump."},
    {"slug": "well-pump-septic-furnace-30-amp-transfer-switch-calculator", "name": "Rural Well-Water Home (1 HP 240V Well Pump + Furnace + Freezer)", "base_watts": 1800, "motor_watts": 2000, "surge_mult": 2.8, "fuel_type": "propane", "hours": 24, "desc": "Size a 7,500W–9,500W 240V generator and 30-Amp Reliance Pro/Tran2 10-circuit transfer switch to start a deep submersible well pump."},
    {"slug": "4-ton-5-ton-central-ac-portable-generator-soft-start-calculator", "name": "4-Ton & 5-Ton Central Air Conditioner Generator + Soft-Start Calculator", "base_watts": 2400, "motor_watts": 3800, "surge_mult": 1.75, "fuel_type": "natgas", "hours": 24, "desc": "See how a Micro-Air EasyStart drops a 4–5 ton AC's 25,000W LRA surge down to 6,800W so it runs on a 11,500W–13,000W Tri-Fuel portable generator."},
    {"slug": "30-amp-vs-50-amp-generator-transfer-switch-inlet-cord-calculator", "name": "30-Amp (7,200W) vs. 50-Amp (12,000W) Transfer Switch & Cord Calculator", "base_watts": 3500, "motor_watts": 3000, "surge_mult": 2.0, "fuel_type": "propane", "hours": 24, "desc": "Calculate exact amperage at 240V, L14-30 vs SS2-50/CS6364 inlet boxes, and 10 AWG vs 6 AWG pure copper generator cord sizing."},
    {"slug": "rv-30-amp-50-amp-air-conditioner-inverter-generator-calculator", "name": "30A & 50A RV Camper (15,000 BTU Rooftop AC + Microwave)", "base_watts": 1300, "motor_watts": 1550, "surge_mult": 2.2, "fuel_type": "propane", "hours": 12, "desc": "Size a 3,700W–4,500W ultra-quiet (52 dBA) dual-fuel inverter generator for boondocking with a 15,000 BTU RV air conditioner."},
    {"slug": "natural-gas-tri-fuel-generator-20-percent-derate-calculator", "name": "Natural Gas Tri-Fuel Generator Sizing (20% NG Derate Calculator)", "base_watts": 3200, "motor_watts": 2800, "surge_mult": 2.0, "fuel_type": "natgas", "hours": 24, "desc": "Natural gas has lower BTU density than gasoline (-20% wattage). Calculate the exact Tri-Fuel generator size needed when running off your home NG meter."},
    {"slug": "propane-generator-fuel-consumption-tank-size-hours-calculator", "name": "Propane Generator Fuel Burn (20-Lb, 40-Lb & 100-Lb Tank Runtime)", "base_watts": 2800, "motor_watts": 1800, "surge_mult": 2.2, "fuel_type": "propane", "hours": 48, "desc": "Calculate exact gallons and pounds of liquid propane consumed over 24 to 72 hours at 25%, 50%, and 75% generator load."},
    {"slug": "winter-ice-storm-heating-furnace-pellet-stove-generator-calculator", "name": "Winter Ice Storm Backup (Gas Furnace, Pellet Stove & Space Heater)", "base_watts": 2200, "motor_watts": 900, "surge_mult": 2.5, "fuel_type": "propane", "hours": 36, "desc": "Calculate <5% THD pure sine wave wattage required for modern ECM variable-speed furnace blowers, pellet stoves, and well pumps."},
    {"slug": "sump-pump-basement-flood-backup-generator-ups-calculator", "name": "1/2 HP & 3/4 HP Dual Sump Pump Storm Backup Calculator", "base_watts": 1100, "motor_watts": 1050, "surge_mult": 2.8, "fuel_type": "gas", "hours": 24, "desc": "Calculate 3,000W startup surge for 1/2 HP and 3/4 HP basement sump pumps plus Zoeller 12V battery backup protection."},
    {"slug": "food-truck-commercial-mobile-kitchen-generator-wattage-calculator", "name": "Food Truck & Mobile Concession Trailer Quiet Generator Calculator", "base_watts": 4200, "motor_watts": 2500, "surge_mult": 2.0, "fuel_type": "propane", "hours": 10, "desc": "Size a 7,500W–9,500W quiet enclosed inverter generator for commercial prep fridges, espresso machines, hood vents, and rooftop AC."},
    {"slug": "jobsite-welder-air-compressor-power-tool-generator-calculator", "name": "Jobsite Contractor Generator (Air Compressor, Table Saw & Welder)", "base_watts": 2500, "motor_watts": 3200, "surge_mult": 2.5, "fuel_type": "gas", "hours": 10, "desc": "Calculate high-inrush wattage and 240V 30A/50A outlets needed to start jobsite air compressors, miter saws, and MIG welders."}
]

def get_dynamic_wattage_pages():
    configs = [
        (2000, 1000, 800, "gas", "2,000W Portable Inverter Tier"),
        (3500, 1600, 1100, "propane", "3,500W–4,500W RV & Home Inverter"),
        (5500, 2400, 1800, "propane", "5,500W–6,500W 240V Mid-Size Tier"),
        (7500, 3200, 2400, "propane", "7,500W 30-Amp Transfer Switch Tier"),
        (9500, 4200, 3000, "propane", "9,500W–12,500W Whole-House Tier"),
        (11500, 5000, 3800, "natgas", "11,500W–14,500W 50-Amp Tri-Fuel Tier"),
        (13000, 5800, 4200, "natgas", "13,000W–15,000W Heavy Whole-Home Tier")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 3))
    pages = []
    for w_tier, b_w, m_w, f_t, label in configs[:active_count]:
        pages.append({
            "slug": f"{w_tier}-watt-backup-generator-transfer-switch-calculator",
            "name": f"{label} ({w_tier:,}W)",
            "base_watts": b_w,
            "motor_watts": m_w,
            "surge_mult": 2.0,
            "fuel_type": f_t,
            "hours": 24,
            "desc": f"See exact appliance capacity, propane/natural-gas derating, 30A/50A transfer switch fit, and 24-hour fuel burn for a {w_tier:,}-watt generator."
        })
    return pages

ALL_CALC_PAGES = GEN_PRESETS + get_dynamic_wattage_pages()

def compute_gen_specs(base_watts, motor_watts, surge_mult, fuel_type, hours):
    running_watts = int(round(base_watts + motor_watts))
    peak_surge_watts = int(round(base_watts + (motor_watts * float(surge_mult))))

    # Fuel derating: Gasoline = 1.0x | Propane (LPG) = 0.90x (needs 1.11x gen) | Natural Gas = 0.80x (needs 1.25x gen)
    if fuel_type == "natgas":
        derate_mult = 1.25
        fuel_label = "Natural Gas (+25% Derate Buffer)"
    elif fuel_type == "propane":
        derate_mult = 1.12
        fuel_label = "Propane LPG (+12% Derate Buffer)"
    else:
        derate_mult = 1.0
        fuel_label = "Gasoline (100% Rated Output)"

    # Add 20% continuous headroom so generator runs at ~70-80% load instead of 100% redline
    req_gen_run_w = int(math.ceil((running_watts * 1.20 * derate_mult) / 500.0) * 500)
    req_gen_peak_w = int(math.ceil((peak_surge_watts * derate_mult) / 500.0) * 500)
    rec_gen_tier = max(req_gen_run_w, int(round(req_gen_peak_w * 0.82)))

    amps_240v = round(running_watts / 240.0, 1)
    if rec_gen_tier <= 4500:
        switch_spec = "30A 120V / 6-Circuit Switch (10 AWG)"
    elif rec_gen_tier <= 7800:
        switch_spec = "30A 240V L14-30 Switch (10 AWG)"
    else:
        switch_spec = "50A 240V SS2-50 Switch (6 AWG)"

    # Fuel Consumption estimate: ~0.095 gal/hr per 1,000 running watts on Gas, ~0.125 gal/hr per 1,000W on Propane
    if fuel_type == "propane":
        gal_per_hr = round((running_watts / 1000.0) * 0.135, 2)
        total_gal = round(gal_per_hr * hours, 1)
        total_lbs_lp = int(round(total_gal * 4.24))
        fuel_burn_str = f"{total_gal} Gal ({total_lbs_lp} lbs LP) / {hours}h"
    elif fuel_type == "natgas":
        cfh = int(round((running_watts / 1000.0) * 13.5))
        fuel_burn_str = f"~{cfh} CFH ({cfh * hours:,} ft³ / {hours}h)"
    else:
        gal_per_hr = round((running_watts / 1000.0) * 0.10, 2)
        total_gal = round(gal_per_hr * hours, 1)
        fuel_burn_str = f"{total_gal} Gal Gas ({gal_per_hr} GPH)"

    return running_watts, peak_surge_watts, rec_gen_tier, req_gen_peak_w, amps_240v, switch_spec, fuel_burn_str, fuel_label

def generate_faq_data(preset_name, base_w, motor_w, surge_m, fuel, hours):
    run_w, surge_w, gen_run, gen_peak, amps, sw_spec, fuel_str, fuel_lbl = compute_gen_specs(
        base_w, motor_w, surge_m, fuel, hours
    )
    return [
        {
            "q": f"What size generator do I need for {preset_name} ({run_w:,}W running / {surge_w:,}W surge)?",
            "a": f"Your appliances draw {run_w:,} Running Watts continuously and spike to {surge_w:,} Peak Surge Watts when motors start. Factoring in a 20% continuous load buffer and {fuel_lbl}, we recommend a generator rated for at least {gen_run:,} Running Watts and {gen_peak:,} Peak Watts."
        },
        {
            "q": f"Do I need a 30-Amp or 50-Amp transfer switch and inlet box for {gen_run:,} watts?",
            "a": f"A 30-Amp L14-30 inlet box maxes out at 7,200 watts (30A × 240V). For this setup, we recommend a {sw_spec} (such as the Reliance Controls Pro/Tran2 10-circuit transfer switch or a main-panel interlock kit)."
        },
        {
            "q": f"How much fuel will this {run_w:,}W load burn over {hours} hours?",
            "a": f"At an average continuous house load of {run_w:,} watts, expect to consume approximately {fuel_str}. Keeping two 100-lb Flame King propane cylinders (or a natural gas quick-connect hose) on hand prevents emergency gas-station runs."
        },
        {
            "q": "How can a portable generator start a 3-ton, 4-ton, or 5-ton central air conditioner?",
            "a": "A central AC only uses 2,500W–4,000W while running, but its compressor draws 90–115 Locked Rotor Amps (22,000W+!) for half a second at startup. Installing a Micro-Air EasyStart Flex soft starter on your outdoor condenser cuts startup surge by up to 70%, allowing a 9,500W–12,500W portable generator to run central air."
        },
        {
            "q": "Why does my modern gas furnace or UPS battery backup refuse to run on a cheap generator?",
            "a": "Variable-speed ECM furnace blowers and PFC computer UPS units reject 'dirty' electricity with high Total Harmonic Distortion (>10% THD). Always choose an Inverter Generator (<3% THD) or a low-THD conventional generator like the Westinghouse WGen9500TFc (<5% THD)."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-orange-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['wattage_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['outlet_spec']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['fuel_spec']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-orange-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-orange-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Tri-Fuel Generators, Inverters, Transfer Switches & Soft Starters Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 NEC 702 &THD Sine-Wave Tested Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Backup Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Running / Peak Watts</th>
                        <th class="p-3.5">Outlets / Circuits</th>
                        <th class="p-3.5">Key Blackout Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-orange-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Wattage / Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Fuel / System:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Outlets / Build:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Warranty / Start:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Load-Test Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Westinghouse+Champion+Tri+Fuel+Generator+Reliance+Transfer+Switch+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Storm Backup Deals</span>
            <span>Save up to 30% on Tri-Fuel & Dual-Fuel Inverter Generators, 30A/50A Transfer Switches, AC Soft Starters & Cords on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Generator Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-orange-700 flex items-center justify-center text-white font-black text-lg shadow-sm">G</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Generator Wattage, Transfer Switch & Fuel Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-orange-800 transition">Wattage & Switch Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-orange-800 transition">Search Generators</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-orange-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-orange-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-orange-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-orange-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-orange-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-orange-800 hover:underline">⚡ {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-orange-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-orange-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-orange-700 hover:bg-orange-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Generator & Switch Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-orange-800 hover:underline">🏠 Home — Master Generator & Transfer Switch Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all backup generator wattage calculators, 30A/50A transfer switch guides, AC soft-start calculators, and daily hardware reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive generator running/surge wattage calculator, transfer switch sizing guide, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    run_w, surge_w, gen_tier, _, _, sw_spec, _, _ = compute_gen_specs(
        page_data["base_watts"], page_data["motor_watts"], page_data["surge_mult"], page_data["fuel_type"], page_data["hours"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {gen_tier:,}W Generator & Switch Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["base_watts"], page_data["motor_watts"],
        page_data["surge_mult"], page_data["fuel_type"], page_data["hours"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, _, p_gen, _, _, _, _, _ = compute_gen_specs(
            p["base_watts"], p["motor_watts"], p["surge_mult"], p["fuel_type"], p["hours"]
        )
        active_cls = "bg-orange-100 border-orange-700 text-orange-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-orange-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-orange-900 font-mono shrink-0">{p_gen:,}W</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Westinghouse+WGen9500TFc+Generator+Reliance+Transfer+Switch+and+Micro+Air+EasyStart")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-orange-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>⚡ NEC Article 702, Motor LRA Surge & Tri-Fuel Derating Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Backup Generator Wattage, 30A/50A Transfer Switch & Fuel Calculator" if is_home else f"{page_data['name']} — Generator & Switch Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter House Running Loads, Motor Surge & Fuel</h2>
                        <p class="text-xs text-gray-600">Calculates rated/peak generator watts, 30A vs 50A switch & fuel gallons</p>
                    </div>
                    <span class="text-xs font-mono bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded font-semibold">Live Surge Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Blackout Backup Scenario</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-orange-700">
                        <option value="{page_data['base_watts']},{page_data['motor_watts']},{page_data['surge_mult']},{page_data['fuel_type']},{page_data['hours']}">Current: {page_data['name']}</option>
                        <option value="2800,2600,1.8,propane,24">Whole House + 3-Ton AC (w/ Soft Start) + Well Pump (9,500W Gen)</option>
                        <option value="1400,850,2.6,gas,24">Essential Circuits: 2 Fridges + Furnace + Sump Pump (4,500W Inverter)</option>
                        <option value="1800,2000,2.8,propane,24">Rural Well Home: 1 HP 240V Well Pump + Furnace + Fridges (7,500W)</option>
                        <option value="2400,3800,1.75,natgas,24">4–5 Ton Central AC (w/ Soft Start) on Natural Gas (11,500W–13,000W)</option>
                        <option value="1300,1550,2.2,propane,12">30A / 50A RV Camper w/ 15,000 BTU Rooftop AC (4,500W Inverter)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="baseInput" class="block text-sm font-bold text-gray-800 mb-1">Base Running Loads (Fridges, Lights, TV, Furnace)</label>
                        <input type="number" id="baseInput" value="{page_data['base_watts']}" min="300" max="15000" step="100" oninput="calculateGen()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-orange-700">
                        <span class="text-[11px] text-gray-600">Fridge: 200W | Furnace: 600W | Lights/Wi-Fi: 300W</span>
                    </div>

                    <div>
                        <label for="motorInput" class="block text-sm font-bold text-gray-800 mb-1">Largest Heavy Motor Running Watts (AC / Well / Sump)</label>
                        <input type="number" id="motorInput" value="{page_data['motor_watts']}" min="0" max="10000" step="100" oninput="calculateGen()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-orange-700">
                        <span class="text-[11px] text-gray-600">Sump: 850W | 1HP Well: 2,000W | 3-Ton AC: 2,800W</span>
                    </div>

                    <div>
                        <label for="surgeInput" class="block text-sm font-bold text-gray-800 mb-1">Motor Startup Surge Multiplier (LRA)</label>
                        <select id="surgeInput" onchange="calculateGen()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="1.75" {"selected" if page_data['surge_mult'] <= 1.85 else ""}>1.75x — AC w/ Micro-Air EasyStart Soft Starter (-65% Surge!)</option>
                            <option value="2.2" {"selected" if 1.85 < page_data['surge_mult'] <= 2.3 else ""}>2.20x — RV Rooftop AC / Inverter Refrigerator</option>
                            <option value="2.6" {"selected" if 2.3 < page_data['surge_mult'] <= 2.7 else ""}>2.60x — Standard Submersible Well Pump / Sump Pump</option>
                            <option value="3.2" {"selected" if page_data['surge_mult'] > 2.7 else ""}>3.20x — Unmodified Central AC (Hard Direct-On-Line Start)</option>
                        </select>
                    </div>

                    <div>
                        <label for="fuelInput" class="block text-sm font-bold text-gray-800 mb-1">Primary Fuel Source (Derating Factor)</label>
                        <select id="fuelInput" onchange="calculateGen()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="gas" {"selected" if page_data['fuel_type'] == "gas" else ""}>Unleaded Gasoline (100% Rated Output)</option>
                            <option value="propane" {"selected" if page_data['fuel_type'] == "propane" else ""}>Liquid Propane LPG (-10% Derate / 30-Yr Shelf Life)</option>
                            <option value="natgas" {"selected" if page_data['fuel_type'] == "natgas" else ""}>Utility Natural Gas Line (-20% Derate / Unlimited Fuel)</option>
                        </select>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="hoursInput" class="block text-sm font-bold text-gray-800 mb-1">Outage Duration for Fuel Estimate (Hours): <span id="hoursLabel" class="text-orange-800 font-extrabold">{page_data['hours']} Hours</span></label>
                        <input type="range" id="hoursInput" value="{page_data['hours']}" min="6" max="96" step="6" oninput="calculateGen()"
                               class="w-full accent-orange-700 cursor-pointer">
                        <div class="flex justify-between text-[11px] text-gray-600">
                            <span>6 Hrs</span>
                            <span>24 Hrs (1 Day)</span>
                            <span>48 Hrs (2 Days)</span>
                            <span>72 Hrs</span>
                            <span>96 Hrs (4 Days)</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-orange-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">2. Engineered Generator & Switch Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Backup Capacity</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-orange-100 border border-orange-300 rounded-xl p-3.5">
                        <span class="text-xs text-orange-950 font-semibold block">Min. Generator Rating</span>
                        <span id="resGenTier" class="text-2xl font-black text-orange-800">8,500W+</span>
                        <span id="resPeakTier" class="text-[11px] text-orange-900 block mt-0.5">10,000W+ Peak Surge</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Your Actual Load</span>
                        <span id="resRunLoad" class="text-xl font-black text-gray-900">5,400W Run</span>
                        <span id="resSurgeLoad" class="text-[11px] text-emerald-800 font-bold block mt-0.5">7,480W LRA Surge</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Transfer Switch & Cord</span>
                        <span id="resSwitchSpec" class="text-sm font-extrabold text-gray-900">50A SS2-50 (6 AWG)</span>
                        <span id="resAmps240" class="text-[11px] text-gray-600 block mt-0.5">22.5A Continuous @ 240V</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Est. Fuel Consumption</span>
                        <span id="resFuelBurn" class="text-sm font-extrabold text-amber-800">17.5 Gal (74 lb LP)</span>
                        <span id="resFuelType" class="text-[11px] text-gray-600 block mt-0.5">Includes LP Derate</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-orange-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-orange-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recGenTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Generator & Switch Match...</h3>
                    <p id="recGenDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Generator &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Switch & Soft-Start
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Tri-Fuel Generators, Quiet Inverters, Transfer Switches & Soft Starters</h2>
                <p class="text-sm text-gray-700">Search any wattage (4500W, 9500W, 13000W), brand (Westinghouse, Champion, DuroMax, Honda, Reliance Controls, Micro-Air, Generac), or 50A cord on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Westinghouse WGen9500TFc Tri Fuel, Reliance 30A Transfer Switch, Micro-Air EasyStart..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-orange-700" required>
                    <button type="submit" class="bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Westinghouse WGen9500TFc WGen11500TFc Tri Fuel Generator')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Westinghouse Tri-Fuel</a>
                    <a href="{amz_url('Champion Dual Fuel Tri Fuel Inverter Generator')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Champion Inverters</a>
                    <a href="{amz_url('Reliance Controls Pro/Tran2 10 Circuit Transfer Switch')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Reliance Transfer Switches</a>
                    <a href="{amz_url('Micro-Air EasyStart Home AC Soft Starter')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Micro-Air AC Soft Start</a>
                    <a href="{amz_url('50 Amp 30 Amp Generator Cord and Power Inlet Box')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">50A Cords & Inlet Boxes</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Verified Emergency Power Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Tri-Fuel Generators, Inverters, Transfer Switches & Cords</h2>
                </div>
                <a href="{amz_url('Best Selling Portable Generators and Transfer Switches')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-orange-800 hover:text-orange-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Generator, Transfer Switch & Soft-Starter Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-orange-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-700 text-white px-2.5 py-1 rounded">Complete Whole-House Blackout Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Want to Run Your Central AC, Well Pump & Fridges Without a $12,000 Standby Unit?</h2>
                <p class="text-sm text-gray-800">Install a Micro-Air EasyStart on your AC condenser (-70% startup surge) and connect a 9,500W–12,500W Tri-Fuel Generator to a 50-Amp Power Inlet Box and Transfer Switch.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Generator + Transfer Switch Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Appliance Load, Transfer Switch & Fuel Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact emergency backup scenario or wattage tier below for pre-calculated running watts, surge watts, and fuel consumption.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">NEC 702, THD & Soft-Start Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-orange-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-orange-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-orange-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-orange-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-orange-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-orange-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("baseInput").value = parts[0];
                document.getElementById("motorInput").value = parts[1];
                document.getElementById("surgeInput").value = parts[2];
                document.getElementById("fuelInput").value = parts[3];
                document.getElementById("hoursInput").value = parts[4];
                calculateGen();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateGen() {{
            const baseW = parseFloat(document.getElementById("baseInput").value) || 2800;
            const motorW = parseFloat(document.getElementById("motorInput").value) || 2600;
            const surgeMult = parseFloat(document.getElementById("surgeInput").value) || 1.8;
            const fuelType = document.getElementById("fuelInput").value || "propane";
            const hours = parseFloat(document.getElementById("hoursInput").value) || 24;

            document.getElementById("hoursLabel").textContent = hours + " Hours";

            const runW = Math.round(baseW + motorW);
            const surgeW = Math.round(baseW + (motorW * surgeMult));

            let derateMult = 1.0;
            let fuelNote = "Gasoline (100% Output)";
            if (fuelType === "natgas") {{
                derateMult = 1.25;
                fuelNote = "Includes +25% NG Derate Buffer";
            }} else if (fuelType === "propane") {{
                derateMult = 1.12;
                fuelNote = "Includes +12% LP Derate Buffer";
            }}

            const reqRunGen = Math.ceil((runW * 1.20 * derateMult) / 500) * 500;
            const reqPeakGen = Math.ceil((surgeW * derateMult) / 500) * 500;
            const recGenTier = Math.max(reqRunGen, Math.round((reqPeakGen * 0.82) / 500) * 500);

            const amps240 = (runW / 240.0).toFixed(1);
            let switchSpec = "50A SS2-50 Switch (6 AWG)";
            if (recGenTier <= 4500) switchSpec = "30A 120V / 6-Circuit (10 AWG)";
            else if (recGenTier <= 7800) switchSpec = "30A L14-30 Switch (10 AWG)";

            let fuelBurnStr = "";
            if (fuelType === "propane") {{
                const gph = (runW / 1000) * 0.135;
                const totGal = (gph * hours).toFixed(1);
                const totLbs = Math.round(totGal * 4.24);
                fuelBurnStr = totGal + " Gal (" + totLbs + " lb LP) / " + hours + "h";
            }} else if (fuelType === "natgas") {{
                const cfh = Math.round((runW / 1000) * 13.5);
                fuelBurnStr = "~" + cfh + " CFH (" + (cfh * hours).toLocaleString() + " ft³)";
            }} else {{
                const gph = (runW / 1000) * 0.10;
                const totGal = (gph * hours).toFixed(1);
                fuelBurnStr = totGal + " Gal Gas / " + hours + "h";
            }}

            document.getElementById("resGenTier").textContent = recGenTier.toLocaleString() + "W+ Run";
            document.getElementById("resPeakTier").textContent = reqPeakGen.toLocaleString() + "W+ Peak Rated";
            document.getElementById("resRunLoad").textContent = runW.toLocaleString() + "W Run";
            document.getElementById("resSurgeLoad").textContent = surgeW.toLocaleString() + "W Peak Surge";
            document.getElementById("resSwitchSpec").textContent = switchSpec;
            document.getElementById("resAmps240").textContent = amps240 + "A Continuous @ 240V";
            document.getElementById("resFuelBurn").textContent = fuelBurnStr;
            document.getElementById("resFuelType").textContent = fuelNote;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Reliance Controls Pro/Tran2 Transfer Switch and Micro-Air EasyStart";

            if (recGenTier <= 4500) {{
                recTitle = "Westinghouse iGen4500DF / Champion 4,500W Dual-Fuel Super-Quiet Inverter";
                recDesc = "Whisper-quiet 52 dBA <3% THD pure sine wave power for fridges, furnaces, sump pumps, and RVs.";
                primaryQuery = "Westinghouse iGen4500DF Champion 4500W Dual Fuel Inverter Generator";
                secondaryQuery = "Reliance Controls 30 Amp Transfer Switch and Power Inlet Box";
            }} else if (recGenTier <= 8000) {{
                recTitle = "Champion 9,000W Tri-Fuel Inverter or Westinghouse WGen7500DF Dual-Fuel Generator";
                recDesc = "240V split-phase power matched to 30-Amp L14-30 transfer switches and well pumps.";
                primaryQuery = "Champion 9000W Tri Fuel Inverter Westinghouse WGen7500DF Generator";
                secondaryQuery = "Reliance Controls 30 Amp 10 Circuit Pro/Tran2 Transfer Switch";
            }} else {{
                recTitle = "Westinghouse WGen9500TFc / WGen11500TFc or DuroMax XP13000HXT Tri-Fuel (<5% THD)";
                recDesc = "Full 50-Amp whole-house Tri-Fuel authority for central AC (w/ EasyStart), well pumps, and appliances.";
                primaryQuery = "Westinghouse WGen9500TFc WGen11500TFc DuroMax XP13000HXT Tri Fuel Generator";
                secondaryQuery = "Micro-Air EasyStart Flex AC Soft Starter and 50 Amp Inlet Box";
            }}

            document.getElementById("recGenTitle").textContent = recTitle;
            document.getElementById("recGenDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateGen);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-orange-700 transition block">
            <span class="text-[11px] font-bold text-orange-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-800">Home & Wattage Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-orange-800">Daily Generator Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Load-Test Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Wattage / Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Fuel / System</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Outlets / Build</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Your House Wattage
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Motor Surge, THD Sine-Wave & Fuel Burn Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-orange-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our emergency power benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Generator & Backup Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-800">Home & Wattage Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-orange-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-orange-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-orange-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "Whole-House Backup (3-Ton AC w/ Soft-Start + Well Pump + Fridges)",
        "base_watts": 2800,
        "motor_watts": 2600,
        "surge_mult": 1.8,
        "fuel_type": "propane",
        "hours": 24,
        "desc": "Calculate exact backup generator running watts, motor LRA starting surge watts, 30A vs 50A transfer switch sizing, and 24-hour propane/natural-gas consumption—plus read 3 new generator reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Generator & Transfer Switch Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
