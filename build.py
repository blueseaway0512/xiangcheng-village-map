import json, os

def build_mobile_responsive_web():
    data_path = 'd:/SynologyDrive/010-PROJECTS/美丽乡村项目/xiangcheng_villages_curated.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        villages = json.load(f)

    # Output directory
    web_dir = 'd:/SynologyDrive/010-PROJECTS/美丽乡村项目/xiangcheng-web'
    os.makedirs(web_dir, exist_ok=True)

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <title>苏州市相城区农村自建房与村落实景数字地图</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
    body, html {{ width: 100%; height: 100%; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", Roboto, "Microsoft YaHei", sans-serif; overflow: hidden; background: #0f172a; }}
    #app {{ display: flex; width: 100%; height: 100%; position: relative; }}
    
    /* Desktop Sidebar */
    #sidebar {{
      width: 360px;
      height: 100%;
      background: #ffffff;
      border-right: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      z-index: 1000;
      box-shadow: 2px 0 12px rgba(0,0,0,0.06);
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .sidebar-header {{
      padding: 16px 18px;
      background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
      color: white;
    }}
    .sidebar-header h1 {{ font-size: 17px; font-weight: 700; margin-bottom: 2px; }}
    .sidebar-header p {{ font-size: 11px; opacity: 0.9; line-height: 1.4; }}
    
    .search-box {{
      padding: 10px 14px;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
    }}
    .search-box input {{
      width: 100%;
      padding: 8px 12px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-size: 13px;
      outline: none;
    }}
    .search-box input:focus {{ border-color: #2563eb; }}
    
    .town-list {{
      flex: 1;
      overflow-y: auto;
      padding: 6px 0;
      -webkit-overflow-scrolling: touch;
    }}
    .town-group {{
      margin-bottom: 4px;
    }}
    .town-title {{
      padding: 8px 16px;
      font-size: 12px;
      font-weight: 700;
      color: #334155;
      background: #f1f5f9;
      border-left: 4px solid #2563eb;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .village-items {{
      list-style: none;
    }}
    .village-item {{
      padding: 10px 18px;
      font-size: 13px;
      color: #334155;
      cursor: pointer;
      border-bottom: 1px solid #f8fafc;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s;
    }}
    .village-item:hover, .village-item:active {{
      background: #eff6ff;
      color: #1d4ed8;
      padding-left: 22px;
    }}
    .village-item.active {{
      background: #dbeafe;
      color: #1e40af;
      font-weight: 600;
      border-left: 3px solid #2563eb;
    }}
    .village-tag {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #e2e8f0;
      color: #64748b;
    }}
    .village-item:hover .village-tag {{
      background: #bfdbfe;
      color: #1e40af;
    }}
    
    /* Footer Tools */
    .sidebar-footer {{
      padding: 12px 14px;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .btn {{
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
      transition: all 0.15s;
    }}
    .btn-primary {{ background: #2563eb; color: white; }}
    .btn-outline {{ background: white; border: 1px solid #cbd5e1; color: #334155; }}
    
    /* Map Area */
    #map-container {{
      flex: 1;
      height: 100%;
      position: relative;
    }}
    #map {{ width: 100%; height: 100%; background: #1e293b; }}
    
    /* Top Toolbar (Desktop) */
    .top-toolbar {{
      position: absolute;
      top: 14px;
      right: 16px;
      z-index: 1000;
      display: flex;
      gap: 6px;
      background: rgba(255, 255, 255, 0.96);
      padding: 6px 10px;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.15);
      backdrop-filter: blur(4px);
    }}
    .tool-btn {{
      padding: 6px 10px;
      font-size: 12px;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      background: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      color: #1e293b;
    }}
    .tool-btn:hover, .tool-btn.active {{
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }}
    
    /* Info Card */
    .info-card {{
      position: absolute;
      bottom: 20px;
      left: 16px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.96);
      padding: 14px 18px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
      max-width: 420px;
      line-height: 1.5;
      font-size: 12px;
      color: #334155;
      backdrop-filter: blur(6px);
      border-left: 4px solid #2563eb;
    }}
    .info-card h3 {{
      font-size: 15px;
      color: #0f172a;
      margin-bottom: 2px;
    }}
    .info-card .coord {{
      font-family: monospace;
      color: #64748b;
      font-size: 11px;
      margin-bottom: 6px;
    }}
    
    #measure-info {{
      position: absolute;
      top: 60px;
      right: 16px;
      z-index: 1000;
      background: rgba(15, 23, 42, 0.9);
      color: #f8fafc;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      display: none;
    }}
    
    /* Floating Mobile Controls (Phone view) */
    .mobile-nav-bar {{
      display: none;
      position: absolute;
      bottom: 20px;
      left: 16px;
      right: 16px;
      z-index: 1100;
      background: rgba(255, 255, 255, 0.96);
      padding: 10px 14px;
      border-radius: 12px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.2);
      backdrop-filter: blur(8px);
      justify-content: space-between;
      align-items: center;
    }}
    .mobile-btn {{
      padding: 8px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      background: #f8fafc;
      color: #1e293b;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .mobile-btn.primary {{
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }}
    
    /* Mobile Drawer (Bottom Sheet) */
    .mobile-drawer-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      z-index: 2000;
    }}
    .mobile-drawer {{
      display: none;
      position: fixed;
      bottom: 0; left: 0; right: 0;
      height: 75%;
      background: white;
      border-radius: 16px 16px 0 0;
      z-index: 2001;
      flex-direction: column;
      box-shadow: 0 -4px 25px rgba(0,0,0,0.25);
      transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .mobile-drawer.open {{
      transform: translateY(0);
    }}
    .drawer-handle {{
      width: 40px;
      height: 4px;
      background: #cbd5e1;
      border-radius: 2px;
      margin: 10px auto 4px auto;
    }}
    
    /* Responsive media queries */
    @media (max-width: 768px) {{
      #sidebar {{
        display: none !important;
      }}
      .top-toolbar {{
        top: 10px;
        right: 10px;
        left: 10px;
        justify-content: space-around;
        padding: 6px;
      }}
      .tool-btn {{
        padding: 5px 8px;
        font-size: 11px;
      }}
      .mobile-nav-bar {{
        display: flex;
      }}
      .info-card {{
        bottom: 80px;
        left: 10px;
        right: 10px;
        max-width: none;
      }}
    }}
  </style>
</head>
<body>
<div id="app">
  <!-- Desktop Sidebar -->
  <div id="sidebar">
    <div class="sidebar-header">
      <h1>相城区农村自建房实景地图</h1>
      <p>苏州市相城区 · 谷歌20级极限航测与宅基地测绘系统</p>
    </div>
    
    <div class="search-box">
      <input type="text" class="search-input" placeholder="搜索村落名称，例如：冯梦龙村、迎湖村..." />
    </div>
    
    <div class="town-list" id="desktopVillageList">
      <!-- Injected list -->
    </div>
    
    <div class="sidebar-footer">
      <button class="btn btn-outline" onclick="locateUser()">
        🧭 定位我的当前位置 (现场实测)
      </button>
      <button class="btn btn-primary" onclick="window.print()">
        🖨️ 打印当前屏幕视野 (A4/A2工程图)
      </button>
    </div>
  </div>
  
  <!-- Map -->
  <div id="map-container">
    <div id="map"></div>
    
    <!-- Top Toolbar -->
    <div class="top-toolbar">
      <button class="tool-btn active" id="btnSatellite" onclick="switchLayer('satellite')">📷 纯卫星图</button>
      <button class="tool-btn" id="btnHybrid" onclick="switchLayer('hybrid')">🛰️ 卫星+路网</button>
      <button class="tool-btn" id="btnTerrain" onclick="switchLayer('terrain')">⛰️ 地形图</button>
      <button class="tool-btn" id="btnMeasureDist" onclick="toggleMeasure('distance')">📏 测距</button>
      <button class="tool-btn" id="btnMeasureArea" onclick="toggleMeasure('area')">📐 测面积</button>
      <button class="tool-btn" onclick="clearMeasurements()">🗑️ 清除</button>
    </div>
    
    <div id="measure-info"></div>
    
    <!-- Info Card -->
    <div class="info-card" id="infoCard">
      <h3 id="cardTitle">黄埭镇 · 冯梦龙村</h3>
      <div class="coord" id="cardCoord">坐标：北纬 31.45950°, 东经 120.52390°</div>
      <p id="cardDesc">全国乡村旅游重点村，新老农房交错，自建房改造与乡村风貌标杆。</p>
      <div style="margin-top: 6px; font-size: 11px; color: #166534; background: #f0fdf4; padding: 4px 8px; border-radius: 4px;">
        🔍 支持 <b>19~20级极限放大</b>，双指张开放大可看清屋顶、院落与间距！
      </div>
    </div>
    
    <!-- Mobile Floating Navigation Bar -->
    <div class="mobile-nav-bar">
      <button class="mobile-btn primary" onclick="openMobileDrawer()">
        📍 选择村庄 (46村)
      </button>
      <button class="mobile-btn" onclick="locateUser()">
        🧭 现场定位
      </button>
      <button class="mobile-btn" onclick="toggleMeasure('distance')">
        📏 测房距
      </button>
    </div>
  </div>
</div>

<!-- Mobile Drawer Modal -->
<div class="mobile-drawer-overlay" id="drawerOverlay" onclick="closeMobileDrawer()"></div>
<div class="mobile-drawer" id="mobileDrawer">
  <div class="drawer-handle"></div>
  <div style="padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0;">
    <h3 style="font-size: 16px; color:#0f172a;">选择相城区村落</h3>
    <button onclick="closeMobileDrawer()" style="background:none; border:none; font-size:18px; color:#64748b; cursor:pointer;">✕</button>
  </div>
  <div class="search-box">
    <input type="text" class="search-input" placeholder="输入村名搜索（如：冯梦龙村、消泾村...）" />
  </div>
  <div class="town-list" id="mobileVillageList"></div>
</div>

<script>
  const villagesData = {json.dumps(villages, ensure_ascii=False)};

  // 1. Initialize Map
  const map = L.map('map', {{
    center: [31.4595, 120.5239],
    zoom: 17,
    zoomControl: false,
    maxZoom: 20
  }});
  L.control.zoom({{ position: 'bottomright' }}).addTo(map);

  // 2. Google Maps Tile Layers (Pure Satellite defaults to active)
  const layerSatellite = L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}', {{
    maxZoom: 20,
    maxNativeZoom: 19,
    attribution: 'Google Satellite'
  }}).addTo(map);

  const layerHybrid = L.tileLayer('https://mt1.google.com/vt/lyrs=y&x={{x}}&y={{y}}&z={{z}}', {{
    maxZoom: 20,
    maxNativeZoom: 19,
    attribution: 'Google Hybrid'
  }});

  const layerTerrain = L.tileLayer('https://mt1.google.com/vt/lyrs=p&x={{x}}&y={{y}}&z={{z}}', {{
    maxZoom: 20,
    maxNativeZoom: 19,
    attribution: 'Google Terrain'
  }});

  let currentLayer = layerSatellite;
  function switchLayer(type) {{
    document.querySelectorAll('.top-toolbar .tool-btn').forEach(b => {{
      if (b.id.startsWith('btnH') || b.id.startsWith('btnS') || b.id.startsWith('btnT')) {{
        b.classList.remove('active');
      }}
    }});
    map.removeLayer(currentLayer);
    if (type === 'satellite') {{
      currentLayer = layerSatellite;
      document.getElementById('btnSatellite').classList.add('active');
    }} else if (type === 'hybrid') {{
      currentLayer = layerHybrid;
      document.getElementById('btnHybrid').classList.add('active');
    }} else if (type === 'terrain') {{
      currentLayer = layerTerrain;
      document.getElementById('btnTerrain').classList.add('active');
    }}
    map.addLayer(currentLayer);
  }}

  // 3. Populate Both Desktop and Mobile Village Lists
  const townGroups = {{}};
  villagesData.forEach(v => {{
    if (!townGroups[v.town]) townGroups[v.town] = [];
    townGroups[v.town].push(v);
  }});

  function renderListInto(containerEl, isMobile) {{
    containerEl.innerHTML = '';
    for (const [town, list] of Object.entries(townGroups)) {{
      const groupDiv = document.createElement('div');
      groupDiv.className = 'town-group';
      
      const titleDiv = document.createElement('div');
      titleDiv.className = 'town-title';
      titleDiv.innerHTML = `<span>${{town}}</span> <span style="font-size:11px; opacity:0.8;">${{list.length}}个村</span>`;
      groupDiv.appendChild(titleDiv);
      
      const ul = document.createElement('ul');
      ul.className = 'village-items';
      
      list.forEach(v => {{
        const li = document.createElement('li');
        li.className = 'village-item';
        li.dataset.name = v.village;
        li.dataset.town = v.town;
        li.innerHTML = `<span>${{v.village}}</span><span class="village-tag">超清航测</span>`;
        
        li.onclick = () => {{
          selectVillage(v);
          if (isMobile) closeMobileDrawer();
        }};
        ul.appendChild(li);

        if (!isMobile) {{
          const marker = L.circleMarker([v.lat, v.lon], {{
            radius: 6,
            fillColor: '#2563eb',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.85
          }}).addTo(map);
          marker.bindTooltip(`<b>${{v.town}} · ${{v.village}}</b>`, {{ direction: 'top', offset: [0, -8] }});
          marker.on('click', () => selectVillage(v));
        }}
      }});
      
      groupDiv.appendChild(ul);
      containerEl.appendChild(groupDiv);
    }}
  }}

  renderListInto(document.getElementById('desktopVillageList'), false);
  renderListInto(document.getElementById('mobileVillageList'), true);

  function selectVillage(v) {{
    document.querySelectorAll('.village-item').forEach(el => {{
      if (el.dataset.name === v.village && el.dataset.town === v.town) {{
        el.classList.add('active');
      }} else {{
        el.classList.remove('active');
      }}
    }});

    map.flyTo([v.lat, v.lon], 18, {{ duration: 1.2 }});

    document.getElementById('cardTitle').innerText = `${{v.town}} · ${{v.village}}`;
    document.getElementById('cardCoord').innerText = `坐标：北纬 ${{v.lat.toFixed(5)}}°, 东经 ${{v.lon.toFixed(5)}}°`;
    document.getElementById('cardDesc').innerText = v.desc || '传统水乡村落，自建房集中连片区域。';
  }}

  // 4. Search Filter
  document.querySelectorAll('.search-input').forEach(input => {{
    input.addEventListener('input', function(e) {{
      const val = e.target.value.trim().toLowerCase();
      document.querySelectorAll('.village-item').forEach(li => {{
        const name = li.dataset.name.toLowerCase();
        const town = li.dataset.town.toLowerCase();
        if (!val || name.includes(val) || town.includes(val)) {{
          li.style.display = 'flex';
        }} else {{
          li.style.display = 'none';
        }}
      }});
    }});
  }});

  // 5. Mobile Drawer Functions
  function openMobileDrawer() {{
    document.getElementById('drawerOverlay').style.display = 'block';
    const drawer = document.getElementById('mobileDrawer');
    drawer.style.display = 'flex';
    setTimeout(() => drawer.classList.add('open'), 10);
  }}
  function closeMobileDrawer() {{
    const drawer = document.getElementById('mobileDrawer');
    drawer.classList.remove('open');
    setTimeout(() => {{
      drawer.style.display = 'none';
      document.getElementById('drawerOverlay').style.display = 'none';
    }}, 300);
  }}

  // 6. User GPS Geolocation
  let userMarker = null;
  function locateUser() {{
    if (!navigator.geolocation) {{
      alert('您的浏览器或设备不支持 GPS 定位');
      return;
    }}
    document.getElementById('measure-info').innerText = '正在获取当前 GPS 现场位置...';
    document.getElementById('measure-info').style.display = 'block';
    
    navigator.geolocation.getCurrentPosition(
      pos => {{
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        map.flyTo([lat, lng], 18, {{ duration: 1.5 }});
        if (userMarker) map.removeLayer(userMarker);
        userMarker = L.circleMarker([lat, lng], {{
          radius: 9,
          fillColor: '#ef4444',
          color: '#ffffff',
          weight: 3,
          opacity: 1,
          fillOpacity: 0.9
        }}).addTo(map);
        userMarker.bindPopup('<b>您当前所在的现场位置</b>').openPopup();
        document.getElementById('measure-info').innerText = `已定位到现场：${{lat.toFixed(5)}}°N, ${{lng.toFixed(5)}}°E`;
        setTimeout(() => {{ document.getElementById('measure-info').style.display = 'none'; }}, 4000);
      }},
      err => {{
        alert('无法获取位置，请在手机上允许浏览器使用位置权限。');
        document.getElementById('measure-info').style.display = 'none';
      }},
      {{ enableHighAccuracy: true, timeout: 10000 }}
    );
  }}

  // 7. Measure Distance & Area Tools
  let measureMode = null;
  let measurePoints = [];
  let measureLine = null;
  let measurePolygon = null;
  let measureMarkers = [];

  function toggleMeasure(mode) {{
    clearMeasurements();
    if (measureMode === mode) {{
      measureMode = null;
      document.getElementById('btnMeasureDist').classList.remove('active');
      document.getElementById('btnMeasureArea').classList.remove('active');
      document.getElementById('measure-info').style.display = 'none';
      return;
    }}
    measureMode = mode;
    document.getElementById('btnMeasureDist').classList.toggle('active', mode === 'distance');
    document.getElementById('btnMeasureArea').classList.toggle('active', mode === 'area');
    const tip = mode === 'distance' 
      ? '请在地图上依次点击两点或多点测量房距/路宽' 
      : '请在地图上依次点击各拐点测量宅基地占地面积';
    document.getElementById('measure-info').innerText = tip;
    document.getElementById('measure-info').style.display = 'block';
  }}

  map.on('click', function(e) {{
    if (!measureMode) return;
    const pt = e.latlng;
    measurePoints.push(pt);

    const m = L.circleMarker(pt, {{ radius: 5, color: '#ef4444', fillColor: '#fff', fillOpacity: 1 }}).addTo(map);
    measureMarkers.push(m);

    if (measureMode === 'distance') {{
      if (measurePoints.length >= 2) {{
        if (measureLine) map.removeLayer(measureLine);
        measureLine = L.polyline(measurePoints, {{ color: '#ef4444', weight: 3, dashArray: '6, 6' }}).addTo(map);
        let dist = 0;
        for (let i = 0; i < measurePoints.length - 1; i++) {{
          dist += measurePoints[i].distanceTo(measurePoints[i+1]);
        }}
        document.getElementById('measure-info').innerText = `测距结果：总长 ${{dist.toFixed(1)}} 米 (${{(dist/1000).toFixed(2)}} 公里)`;
      }}
    }} else if (measureMode === 'area') {{
      if (measurePoints.length >= 3) {{
        if (measurePolygon) map.removeLayer(measurePolygon);
        measurePolygon = L.polygon(measurePoints, {{ color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.25 }}).addTo(map);
        const area = calcPolygonArea(measurePoints);
        document.getElementById('measure-info').innerText = `测面结果：宅基地面积约 ${{area.toFixed(1)}} ㎡ (约 ${{ (area * 0.0015).toFixed(2) }} 亩)`;
      }}
    }}
  }});

  function clearMeasurements() {{
    measurePoints = [];
    if (measureLine) {{ map.removeLayer(measureLine); measureLine = null; }}
    if (measurePolygon) {{ map.removeLayer(measurePolygon); measurePolygon = null; }}
    measureMarkers.forEach(m => map.removeLayer(m));
    measureMarkers = [];
    document.getElementById('measure-info').style.display = 'none';
  }}

  function calcPolygonArea(latlngs) {{
    const radius = 6378137;
    let area = 0;
    const len = latlngs.length;
    if (len < 3) return 0;
    for (let i = 0; i < len; i++) {{
      const p1 = latlngs[i];
      const p2 = latlngs[(i + 1) % len];
      area += ((p2.lng - p1.lng) * (Math.PI / 180)) * (2 + Math.sin(p1.lat * (Math.PI / 180)) + Math.sin(p2.lat * (Math.PI / 180)));
    }}
    area = area * radius * radius / 2.0;
    return Math.abs(area);
  }}
</script>
</body>
</html>
'''
    index_file = os.path.join(web_dir, 'index.html')
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # Also update the local one in 相城区村落实景规划图集
    local_file = 'd:/SynologyDrive/010-PROJECTS/美丽乡村项目/相城区村落实景规划图集/相城区村落实景数字地图.html'
    with open(local_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print('Generated responsive index.html successfully:', index_file)

if __name__ == '__main__':
    build_mobile_responsive_web()
