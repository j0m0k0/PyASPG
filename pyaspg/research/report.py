"""Self-contained SVG/HTML reporting for research simulation results."""

from __future__ import annotations

import csv
import html
import json
import os
from typing import Any

from .simulator import SimulationResult


def _chart(rows: list[dict[str, Any]], keys: list[tuple[str, str]], title: str, unit: str) -> str:
    width, height, left, right, top, bottom = 860, 310, 70, 24, 38, 46
    vals = [float(row[key]) for row in rows for key, _ in keys]
    ymax = max(vals, default=1.0) or 1.0
    ymax *= 1.12
    plot_w, plot_h = width - left - right, height - top - bottom
    colors = ["#69e0c2", "#ffb86b", "#fb7185", "#8ab4ff"]
    pieces = [f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
              f'<text x="{left}" y="22" class="chart-title">{html.escape(title)}</text>']
    for i in range(5):
        y = top + plot_h * i / 4
        pieces.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="gridline"/>')
        pieces.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" class="axis">{ymax*(1-i/4):,.2f}</text>')
    for n, (key, label) in enumerate(keys):
        coords = []
        for ix, row in enumerate(rows):
            x = left + plot_w * ix / max(1, len(rows) - 1)
            y = top + plot_h * (1 - float(row[key]) / ymax)
            coords.append(f"{x:.1f},{y:.1f}")
        pieces.append(f'<polyline points="{" ".join(coords)}" fill="none" stroke="{colors[n % len(colors)]}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
        lx = left + n * 185
        pieces.append(f'<line x1="{lx}" y1="{height-15}" x2="{lx+20}" y2="{height-15}" stroke="{colors[n % len(colors)]}" stroke-width="3"/><text x="{lx+27}" y="{height-11}" class="legend">{html.escape(label)}</text>')
    active = [r["timestep"] for r in rows if r["attack_active"]]
    if active:
        x1 = left + plot_w * active[0] / max(1, len(rows) - 1)
        x2 = left + plot_w * active[-1] / max(1, len(rows) - 1)
        pieces.insert(2, f'<rect x="{x1:.1f}" y="{top}" width="{max(2, x2-x1):.1f}" height="{plot_h}" fill="#fb7185" opacity=".08"/>')
        pieces.append(f'<text x="{left}" y="{height-30}" class="attack-label">Attack window</text>')
    pieces.append(f'<text x="{left}" y="{height-2}" class="axis">Time step</text><text transform="translate(15 {top+plot_h/2}) rotate(-90)" class="axis" text-anchor="middle">{html.escape(unit)}</text></svg>')
    return "".join(pieces)


def _topology_svg(result: SimulationResult) -> str:
    topology, cfg = result.topology, result.config
    stations = len(topology["substation_prosumers"])
    width, height = 920, 300
    parts = [f'<svg viewBox="0 0 {width} {height}" class="topology" role="img" aria-label="Grid topology and customer counts">',
             '<defs><linearGradient id="node" x1="0" x2="1"><stop stop-color="#172a45"/><stop offset="1" stop-color="#20395b"/></linearGradient></defs>',
             '<text x="24" y="28" class="chart-title">Physical load topology</text>']
    a_count = len(topology["aggregator_prosumers"])
    for a, count in enumerate(topology["aggregator_prosumers"]):
        x, y = 28, 57 + a * (215 / max(1, a_count))
        highlight = a == cfg["compromised_aggregator"] and cfg["attack"] != "none"
        color = "#fb7185" if highlight else "#69e0c2"
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="176" height="31" rx="10" fill="url(#node)" stroke="{color}" stroke-width="1.5"/>')
        label = f"Aggregator {a+1}" + (" · compromised" if highlight else "")
        parts.append(f'<text x="{x+12}" y="{y+20:.1f}" class="node-label">{label}</text><text x="{x+162}" y="{y+20:.1f}" text-anchor="end" class="node-count">{count}</text>')
        total = max(1, count)
        for s in range(stations):
            joint = topology["joint_counts"][a][s]
            target_y = 72 + s * (175 / max(1, stations - 1))
            x2 = 728
            parts.append(f'<path d="M 204 {y+15.5:.1f} C 380 {y+15.5:.1f}, 510 {target_y:.1f}, {x2} {target_y:.1f}" fill="none" stroke="{color}" stroke-opacity=".23" stroke-width="{1+6*joint/total:.1f}"/>')
    for s, count in enumerate(topology["substation_prosumers"]):
        y = 55 + s * (190 / max(1, stations - 1))
        parts.append(f'<rect x="728" y="{y:.1f}" width="164" height="42" rx="12" fill="#172a45" stroke="#8ab4ff"/>')
        parts.append(f'<text x="742" y="{y+18:.1f}" class="node-label">Substation {s+1}</text><text x="742" y="{y+34:.1f}" class="node-count">{count} prosumers</text>')
    parts.append('<text x="28" y="286" class="axis">Line width reflects prosumer count · pink marks compromised aggregator</text></svg>')
    return "".join(parts)


def render_report(result: SimulationResult, output_dir: str, title: str = "PyASPG · Grid resilience lab") -> str:
    """Write detailed CSV/JSON and a polished, portable HTML dashboard."""
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "timeseries.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result.series[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(result.series)
    with open(os.path.join(output_dir, "metrics.json"), "w", encoding="utf-8") as stream:
        json.dump({"config": result.config, "metrics": result.metrics, "topology": result.topology}, stream, indent=2)
    rows = result.series
    summary = result.metrics
    cards = [
        ("Deviation from nominal", f"{summary['deviation_from_nominal']*100:.2f}%", "generation shift vs secure case"),
        ("Outage intensity", f"{summary['power_outage_count']:.2f}", "substation outages / time step"),
        ("Potential outage risk", f"{summary['potential_outage_risk']*100:.1f}%", "attack-window steps below NSR threshold"),
        ("Unserved energy", f"{summary['unserved_energy']:.2f}", "kWh over the attack window"),
        ("Redistribution cost", f"{summary['redistribution_cost']:,.1f}", "distance- and reliability-weighted"),
        ("Energy waste", f"{summary['energy_waste']:,.2f}", "kWh surplus after load and line losses"),
    ]
    metric_html = "".join(f'<article class="metric"><div class="metric-label">{html.escape(k)}</div><div class="metric-value">{v}</div><div class="metric-note">{html.escape(n)}</div></article>' for k,v,n in cards)
    report = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<style>
:root{{--bg:#0a1220;--panel:#111e30;--line:#253750;--ink:#edf5ff;--muted:#91a6bd;--mint:#69e0c2;--blue:#8ab4ff;--rose:#fb7185;--amber:#ffb86b}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(ellipse at 78% -5%,#19324a 0,transparent 38%),var(--bg);color:var(--ink);font:15px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}main{{max-width:1220px;margin:auto;padding:42px 30px 56px}}.eyebrow{{color:var(--mint);font-size:12px;text-transform:uppercase;letter-spacing:.18em;font-weight:700}}h1{{font-size:clamp(32px,5vw,52px);line-height:1.05;margin:12px 0}}.lede{{max-width:790px;color:var(--muted);font-size:17px}}.hero{{display:flex;justify-content:space-between;gap:30px;align-items:flex-start;margin-bottom:30px}}.badge{{white-space:nowrap;border:1px solid #34506e;border-radius:99px;padding:9px 14px;color:var(--blue);font-size:13px}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0}}.metric,.panel{{background:linear-gradient(140deg,#142238,#0f1a2b);border:1px solid var(--line);border-radius:16px}}.metric{{padding:18px 20px}}.metric-label{{color:var(--muted);font-size:13px}}.metric-value{{font-size:30px;letter-spacing:-.04em;font-weight:700;margin:5px 0}}.metric-note,.caption{{color:var(--muted);font-size:12px}}.panel{{padding:20px;margin:14px 0}}.panel h2{{font-size:17px;margin:0 0 12px}}.chart,.topology{{width:100%;height:auto;overflow:visible}}.gridline{{stroke:#293a50;stroke-width:1}}.chart-title{{fill:var(--ink);font-size:14px;font-weight:700}}.axis,.legend,.node-count{{fill:var(--muted);font-size:10px}}.legend{{font-size:11px}}.attack-label{{fill:var(--rose);font-size:10px}}.node-label{{fill:var(--ink);font-size:12px}}.node-count{{font-size:11px}}.cols{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}.method{{display:flex;gap:12px;align-items:center;color:var(--muted);font-size:13px}}.step{{border:1px solid var(--line);border-radius:10px;padding:12px 14px;flex:1;text-align:center;background:#101c2d}}.arrow{{color:var(--mint);font-size:21px}}.foot{{margin-top:24px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:16px}}a{{color:var(--mint)}}@media(max-width:760px){{main{{padding:24px 16px}}.hero{{display:block}}.badge{{display:inline-block;margin-top:14px}}.metrics{{grid-template-columns:repeat(2,1fr)}}.cols{{grid-template-columns:1fr}}.method{{flex-wrap:wrap}}.step{{min-width:40%}}}}@media(max-width:440px){{.metrics{{grid-template-columns:1fr}}}}
</style><body><main><header class="hero"><div><div class="eyebrow">Topology-aware smart grid simulation</div><h1>{html.escape(title)}</h1><p class="lede">A paired secure-versus-compromised experiment. Inspect how aggregator concentration, physical substation placement and FDIA strategy reshape reliability, loss and recovery.</p></div><div class="badge">seed {result.config['seed']} · {result.config['steps']} steps · {result.config['prosumers']} prosumers</div></header>
<section class="metrics">{metric_html}</section><section class="panel"><h2>Power balance through time</h2>{_chart(rows, [('actual_demand','Actual demand'),('reported_demand','Reported demand'),('generated_power','Generated power'),('secure_generation','Secure generation')], 'Reported load and dispatch', 'Power units')}<div class="caption">Shaded interval marks the attack window. Secure generation is the paired reference run on the same topology and load profile.</div></section>
<section class="panel"><h2>Grid connectivity under attack</h2>{_topology_svg(result)}</section><div class="cols"><section class="panel"><h2>Outage and risk signals</h2>{_chart(rows, [('outage_substations','Outage substations'),('por_event','Potential outage risk')], 'Localized reliability signals', 'Count / ratio')}</section><section class="panel"><h2>How a scenario is evaluated</h2><div class="method"><div class="step">Generate demand<br>+ renewable profile</div><span class="arrow">→</span><div class="step">Map customers to<br>aggregators + substations</div><span class="arrow">→</span><div class="step">Inject FDIA and<br>dispatch generation</div><span class="arrow">→</span><div class="step">Measure outages,<br>risk, cost and waste</div></div><p class="caption">Metrics follow the paper’s Deviation from Nominal, Power Outage Count, Redistribution Cost and Potential Outage Risk definitions, with unserved energy and energy waste added for operational context.</p></section></div>
<footer class="foot">Research abstraction for scenario analysis, not an AC power-flow, protection coordination or operational planning tool. Raw values: <a href="timeseries.csv">timeseries.csv</a> · <a href="metrics.json">metrics.json</a>.</footer></main></body></html>'''
    path = os.path.join(output_dir, "report.html")
    with open(path, "w", encoding="utf-8") as stream: stream.write(report)
    return path
