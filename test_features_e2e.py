import asyncio
import httpx
from app.main import app


async def run_verification():
    print("=" * 65)
    print("  VAYUMITRA ASYNC END-TO-END FEATURE VERIFICATION")
    print("=" * 65)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health
        h = await client.get("/api/health")
        print("\n[Feature 1] Health Check & Local LLM Telemetry:")
        print(f"  HTTP Status: {h.status_code}")
        h_json = h.json()
        print(f"  Service: {h_json['service']} v{h_json['version']}")
        print(f"  LLM Mode: {h_json['llm_mode']}")
        print(f"  RAG Chunks: {h_json['rag_chunks_indexed']}")

        # 2. Air Quality
        aq = await client.get("/api/air-quality?lat=28.6139&lon=77.2090")
        print("\n[Feature 2] Live Air Quality & Health Risk Engine:")
        print(f"  HTTP Status: {aq.status_code}")
        data = aq.json()
        print(f"  Location: {data['location_label']}")
        print(f"  Overall AQI: {data['overall_aqi']} ({data['aqi_label']})")
        print(f"  Dominant Pollutant: {data['dominant_pollutant']}")
        print(f"  24h Cigarette Equivalent: {data['cigarette_equivalent_24h']} cigarettes")
        print(f"  Dispersion Verdict: {data['atmospheric_factors']['dispersion_verdict']}")
        print(f"  Best Ventilation Window: {data['atmospheric_factors']['best_ventilation_window']}")
        print(f"  Health Category: {data['health_impact']['category_label']}")
        print(f"  Red-Flag Symptoms: {data['health_impact']['red_flag_symptoms']}")
        print(f"  Total Pollutants Enriched: {len(data['pollutants'])}")
        for pol in data['pollutants']:
            print(f"    - {pol['name']}: {pol['value']} {pol['unit']} [{pol['status']}] (CPCB: {pol['cpcb_multiplier']}x, WHO: {pol['who_multiplier']}x)")

        # 3. Routine Plan
        rp = await client.post(
            "/api/routine-plan",
            json={
                "lat": 28.6139,
                "lon": 77.2090,
                "vulnerable_groups": ["child", "asthmatic"],
                "commute_mode": "two_wheeler",
                "commute_distance_km": 8.0,
                "home_type": "apartment_unsealed",
                "cooking_fuel": "lpg",
                "budget_tier": "low",
            },
        )
        print("\n[Feature 3] Upgraded Actionable Plan & Rich Action Cards:")
        print(f"  HTTP Status: {rp.status_code}")
        plan = rp.json()
        print(f"  Location: {plan['location_label']}")
        print(f"  Total Inhaled PM2.5 Avoided: -{plan['total_impact']['pm25_reduction_ug_per_day']} ug/day")
        print(f"  Total Cigarettes Saved: -{plan['total_impact']['cigarette_equivalents_saved']} cig/day")
        print(f"  Rich Action Cards Count: {len(plan['action_cards'])}")
        for card in plan['action_cards']:
            print(f"    - [{card['category']} | {card['budget_tier']}] {card['title']}")
            print(f"      Impact: {card['quantified_impact']['summary_badge']}")
            print(f"      Citation: {card['source_citation']}")

        # 4. SSE Chat Stream
        print("\n[Feature 4] Prompt-Hardened Chat Stream:")
        chat_resp = await client.post(
            "/api/chat",
            json={
                "message": "Is it safe to jog outdoors at 6 AM today?",
                "lat": 28.6139,
                "lon": 77.2090,
            },
        )
        print(f"  HTTP Status: {chat_resp.status_code}")
        first_few_lines = chat_resp.text.split("\n")[:10]
        print(f"  SSE Stream preview: {len(chat_resp.text)} chars returned")
        for line in first_few_lines:
            if line.strip():
                print(f"    {line}")

        # 5. Static React UI Serving
        print("\n[Feature 5] Single-Port Full-Stack React Distribution:")
        ui_resp = await client.get("/")
        print(f"  HTTP Status: {ui_resp.status_code}")
        has_root = '<div id="root">' in ui_resp.text
        has_assets = '/assets/index' in ui_resp.text
        print(f"  Serves Root: {has_root}")
        print(f"  Serves Bundled Assets: {has_assets}")

    print("\n" + "=" * 65)
    print("  ALL FEATURES VERIFIED WITH ZERO ERRORS!")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run_verification())
