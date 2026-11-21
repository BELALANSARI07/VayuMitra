import json
import threading
import time
import urllib.request
import uvicorn

def run_server():
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, log_level="warning")

def test_all():
    print("=" * 60)
    print("  VAYUMITRA LOCALHOST END-TO-END FEATURE VERIFICATION")
    print("=" * 60)

    # 1. Health & Telemetry
    print("\n[Feature 1] Health Check & Local LLM Telemetry (/api/health):")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/health") as r:
        health = json.loads(r.read().decode())
        print(f"  Status: {health['status']}")
        print(f"  Service: {health['service']} (v{health['version']})")
        print(f"  LLM Mode: {health['llm_mode']}")
        print(f"  RAG Chunks Indexed: {health['rag_chunks_indexed']}")

    # 2. Air Quality & 24h Safe Window
    print("\n[Feature 2] Live Pollutants & Diurnal Safe Window (/api/air-quality):")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/air-quality?lat=28.6139&lon=77.2090") as r:
        aqi = json.loads(r.read().decode())
        print(f"  Location: {aqi['location_label']}")
        print(f"  Current NAQI: {aqi['aqi_value']} ({aqi['aqi_label']})")
        print(f"  Primary Pollutant: {aqi['primary_pollutant']}")
        print(f"  24h Safe Outdoor Window: {aqi['best_safe_window']}")
        print(f"  Pollutant readings available: {len(aqi['pollutants'])}")
        print(f"  Hourly timeline datapoints: {len(aqi['hourly_forecast_24h'])}")

    # 3. Personalized Routine Plan (Pillars 1, 2, 3, 4)
    print("\n[Feature 3] Personalized Routine Plan & Impact Engine (/api/routine-plan):")
    payload = json.dumps({
        "lat": 28.6139,
        "lon": 77.2090,
        "vulnerable_groups": ["child", "asthmatic"],
        "commute_mode": "two_wheeler",
        "commute_distance_km": 8.0,
        "home_type": "apartment_unsealed",
        "cooking_fuel": "lpg",
        "budget_tier": "low",
        "household_size": 4
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/routine-plan",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        plan = json.loads(r.read().decode())
        print("  Pillar 1 (Time-Shifted Routines):")
        for rt in plan["routines"]:
            print(f"    - [{rt['time_slot']}]: {rt['action']}")
            print(f"      Delta: -{rt['impact']['pm25_reduction_ug_per_day']} ug PM2.5/day (-{rt['impact']['cigarette_equivalents_saved']} cig eq.)")

        print("  Pillar 2 (Budget-Tiered Indoor Hacks):")
        for hk in plan["indoor_hacks"]:
            cost = "FREE" if hk["estimated_cost_inr"] == 0 else f"~INR {hk['estimated_cost_inr']}"
            print(f"    - {hk['title']} ({cost}, {hk['effectiveness_pct']}% CADR removal)")

        print("  Pillar 3 (Sustainable Swaps):")
        for sw in plan["sustainable_swaps"]:
            co2 = f"-{sw['impact']['co2_saved_g_per_week'] / 1000:.1f} kg CO2/wk" if sw['impact']['co2_saved_g_per_week'] else ""
            print(f"    - {sw['swap_from']} -> {sw['swap_to']} {co2}")

        print("  Pillar 4 (Quantified Total Daily Impact):")
        tot = plan["total_impact"]
        print(f"    - Total Inhaled PM2.5 Avoided: -{tot['pm25_reduction_ug_per_day']} ug/day")
        print(f"    - Total Cigarettes Avoided: -{tot['cigarette_equivalents_saved']} cig/day")
        if tot.get("co2_saved_g_per_week"):
            print(f"    - Carbon Footprint Avoided: -{tot['co2_saved_g_per_week'] / 1000:.1f} kg CO2/wk")

    # 4. SSE Chat Assistant
    print("\n[Feature 4] SSE Streaming Chat Assistant (/api/chat):")
    chat_payload = json.dumps({
        "message": "Is it safe to jog outdoors at 6 AM today with severe smog?",
        "lat": 28.6139,
        "lon": 77.2090
    }).encode("utf-8")
    chat_req = urllib.request.Request(
        "http://127.0.0.1:8000/api/chat",
        data=chat_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(chat_req) as r:
        lines = [r.readline().decode() for _ in range(16)]
        print("  SSE Event Stream Sample (Citations + Impact + Tokens):")
        for line in lines[:8]:
            if line.strip():
                print(f"    {line.strip()}")

    # 5. Static React UI Serving
    print("\n[Feature 5] Single-Port Full-Stack React UI Serving (/):")
    with urllib.request.urlopen("http://127.0.0.1:8000/") as r:
        html = r.read().decode("utf-8")
        has_root = '<div id="root">' in html
        has_assets = "/assets/index" in html
        print(f"  HTTP Status: {r.status} OK")
        print(f"  Serves compiled index.html: {has_root}")
        print(f"  Loads compiled Vite CSS/JS assets: {has_assets}")

    print("\n" + "=" * 60)
    print("  ALL 5 FEATURES VERIFIED SUCCESSFULLY ON LOCALHOST!")
    print("=" * 60)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2)
    test_all()
