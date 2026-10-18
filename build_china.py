import json, os

def build_china_friendly_web():
    data_path = 'd:/SynologyDrive/010-PROJECTS/美丽乡村项目/xiangcheng_villages_curated.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        villages = json.load(f)

    web_dir = 'd:/SynologyDrive/010-PROJECTS/美丽乡村项目/xiangcheng-web'
    os.makedirs(web_dir, exist_ok=True)

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <title>苏州市相城区农村自建房与村落实景数字地图 (国内免翻墙极速版)</title>
  <!-- 国内极速 CDN (360 宝塔前端公共库，国内秒开) -->
  <link rel="stylesheet" href="https://lib.baomitu.com/leaflet/1.9.4/leaflet.css" />
  <script src="https://lib.baomitu.com/leaflet/1.9.4/leaflet.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
    body, html {{ width: 100%; height: 100%; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", Roboto, "Microsoft YaHei", sans-serif; overflow: hidden; background: #0f172a; }}
    #app {{ display: flex; width: 100%; height: 100%; position: relative; }}
    
    #sidebar {{
      width: 360px;
      height: 100%;
      background: #ffffff;
      border-right: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      z-index: 1000;
      box-shadow: 2px 0 12px rgba(0,0,0,0.06);
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
    .town-group {{ margin-bottom: 4px; }}
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
    .village-items {{ list-style: none; }}
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
    
    #map-container {{ flex: 1; height: 100%; position: relative; }}
    #map {{ width: 100%; height: 100%; background: #1e293b; }}
    
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
    
    .info-card {{
      position: absolute;
      bottom: 20px;
      left: 16px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.96);
      padding: 14px 18px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
      max-width: 440px;
      line-height: 1.5;
      font-size: 12px;
      color: #334155;
      backdrop-filter: blur(6px);
      border-left: 4px solid #2563eb;
    }}
    .info-card h3 {{ font-size: 15px; color: #0f172a; margin-bottom: 2px; }}
    .info-card .coord {{ font-family: monospace; color: #64748b; font-size: 11px; margin-bottom: 6px; }}
    
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
    .mobile-btn.primary {{ background: #2563eb; color: white; border-color: #2563eb; }}
    
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
    .mobile-drawer.open {{ transform: translateY(0); }}
    .drawer-handle {{ width: 40px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 10px auto 4px auto; }}
    
    @media (max-width: 768px) {{
      #sidebar {{ display: none !important; }}
      .top-toolbar {{ top: 10px; right: 10px; left: 10px; justify-content: space-around; padding: 6px; }}
      .tool-btn {{ padding: 5px 8px; font-size: 11px; }}
      .mobile-nav-bar {{ display: flex; }}
      .info-card {{ bottom: 80px; left: 10px; right: 10px; max-width: none; }}
    }}
  </style>
</head>
<body>
<div id="app">
  <div id="sidebar">
    <div class="sidebar-header">
      <h1>相城区农村自建房实景地图</h1>
      <p>苏州市相城区 · 国内免翻墙直连航测与宅基地测绘系统</p>
    </div>
    <div class="search-box">
      <input type="text" class="search-input" placeholder="搜索村落名称，例如：冯梦龙村、迎湖村..." />
    </div>
    <div class="town-list" id="desktopVillageList"></div>
    <div class="sidebar-footer">
      <button class="btn btn-outline" onclick="locateUser()">🧭 定位我的当前位置 (现场实测)</button>
      <button class="btn btn-primary" onclick="window.print()">🖨️ 打印当前屏幕视野 (工程底图)</button>
    </div>
  </div>
  
  <div id="map-container">
    <div id="map"></div>
    <div class="top-toolbar">
      <button class="tool-btn active" id="btnAmap" onclick="switchLayer('amap')">🇨🇳 高德实景(国内秒开)</button>
      <button class="tool-btn" id="btnEsri" onclick="switchLayer('esri')">🛰️ Esri航测(免翻墙)</button>
      <button class="tool-btn" id="btnGoogle" onclick="switchLayer('google')">🌍 谷歌实景(需翻墙)</button>
      <div style="width: 1px; background:#cbd5e1; margin: 0 4px;"></div>
      <button class="tool-btn" id="btnMeasureDist" onclick="toggleMeasure('distance')">📏 测房距</button>
      <button class="tool-btn" id="btnMeasureArea" onclick="toggleMeasure('area')">📐 测面积</button>
      <button class="tool-btn" onclick="clearMeasurements()">🗑️ 清除</button>
    </div>
    
    <div id="measure-info"></div>
    
    <div class="info-card" id="infoCard">
      <h3 id="cardTitle">黄埭镇 · 冯梦龙村</h3>
      <div class="coord" id="cardCoord">坐标：北纬 31.45950°, 东经 120.52390°</div>
      <p id="cardDesc">全国乡村旅游重点村，新老农房交错，自建房改造与乡村风貌标杆。</p>
      <div style="margin-top: 6px; font-size: 11px; color: #166534; background: #f0fdf4; padding: 4px 8px; border-radius: 4px;">
        ⚡ <b>国内直连提示</b>：默认采用国内机房高德高清遥感与 Esri 卫星，国内客户手机打开 100% 免翻墙秒开！
      </div>
    </div>
    
    <div class="mobile-nav-bar">
      <button class="mobile-btn primary" onclick="openMobileDrawer()">📍 选择村庄 ({len(villages)}村)</button>
      <button class="mobile-btn" onclick="locateUser()">🧭 现场定位</button>
      <button class="mobile-btn" onclick="toggleMeasure('distance')">📏 测房距</button>
    </div>
  </div>
</div>

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
  // 1. WGS-84 to GCJ-02 Coordinate Converter (Sub-meter accuracy)
  function wgs84ToGcj02(lat, lon) {{
    const a = 6378245.0, ee = 0.00669342162296594323;
    function transformLat(x, y) {{
      let ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(Math.abs(x));
      ret += (20.0 * Math.sin(6.0 * x * Math.PI) + 20.0 * Math.sin(2.0 * x * Math.PI)) * 2.0 / 3.0;
      ret += (20.0 * Math.sin(y * Math.PI) + 40.0 * Math.sin(y / 3.0 * Math.PI)) * 2.0 / 3.0;
      ret += (160.0 * Math.sin(y / 12.0 * Math.PI) + 320 * Math.sin(y * Math.PI / 30.0)) * 2.0 / 3.0;
      return ret;
    }}
    function transformLon(x, y) {{
      let ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(Math.abs(x));
      ret += (20.0 * Math.sin(6.0 * x * Math.PI) + 20.0 * Math.sin(2.0 * x * Math.PI)) * 2.0 / 3.0;
      ret += (20.0 * Math.sin(x * Math.PI) + 40.0 * Math.sin(x / 3.0 * Math.PI)) * 2.0 / 3.0;
      ret += (150.0 * Math.sin(x / 12.0 * Math.PI) + 300.0 * Math.sin(x / 30.0 * Math.PI)) * 2.0 / 3.0;
      return ret;
    }}
    const dlat = transformLat(lon - 105.0, lat - 35.0);
    const dlon = transformLon(lon - 105.0, lat - 35.0);
    const radlat = lat / 180.0 * Math.PI;
    let magic = Math.sin(radlat);
    magic = 1 - ee * magic * magic;
    const sqrtmagic = Math.sqrt(magic);
    const finalLat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * Math.PI);
    const finalLon = (dlon * 180.0) / (a / sqrtmagic * Math.cos(radlat) * Math.PI);
    return [lat + finalLat, lon + finalLon];
  }}

  const rawVillages = {json.dumps(villages, ensure_ascii=False)};
  // Pre-calculate GCJ-02 coordinates for seamless domestic map alignment
  const villagesData = rawVillages.map(v => {{
    const [glat, glon] = wgs84ToGcj02(v.lat, v.lon);
    return {{ ...v, gcj_lat: glat, gcj_lon: glon }};
  }});

  let currentCoordSys = 'gcj02'; // 'gcj02' for Amap, 'wgs84' for Esri/Google

  // 2. Initialize Leaflet Map (Centered on Fengmenglong in GCJ-02)
  const initCoord = wgs84ToGcj02(31.4595, 120.5239);
  const map = L.map('map', {{
    center: initCoord,
    zoom: 17,
    zoomControl: false,
    maxZoom: 20
  }});
  L.control.zoom({{ position: 'bottomright' }}).addTo(map);

  // 3. Tile Layers:
  // Layer 1: 高德卫星图 (国内阿里云服务器，免翻墙极速秒开)
  const layerAmapSat = L.tileLayer('https://webst0{{s}}.is.autonavi.com/appmaptile?style=6&x={{x}}&y={{y}}&z={{z}}', {{
    subdomains: ['1', '2', '3', '4'],
    maxZoom: 20,
    maxNativeZoom: 18,
    attribution: '高德地图卫星遥感 (国内免翻墙)'
  }}).addTo(map);

  // Layer 2: Esri World Imagery (ArcGIS 全球遥感底图，国内直连免翻墙)
  const layerEsri = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
    maxZoom: 20,
    maxNativeZoom: 18,
    attribution: 'Esri World Imagery (免翻墙)'
  }});

  // Layer 3: 谷歌卫星 (全球亚米级，需翻墙环境)
  const layerGoogle = L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}', {{
    maxZoom: 20,
    maxNativeZoom: 19,
    attribution: 'Google Satellite'
  }});

  let activeTileLayer = layerAmapSat;

  function switchLayer(type) {{
    document.querySelectorAll('.top-toolbar .tool-btn').forEach(b => {{
      if (b.id.startsWith('btnA') || b.id.startsWith('btnE') || b.id.startsWith('btnG')) b.classList.remove('active');
    }});
    map.removeLayer(activeTileLayer);

    const oldCoordSys = currentCoordSys;
    if (type === 'amap') {{
      activeTileLayer = layerAmapSat;
      currentCoordSys = 'gcj02';
      document.getElementById('btnAmap').classList.add('active');
    }} else if (type === 'esri') {{
      activeTileLayer = layerEsri;
      currentCoordSys = 'wgs84';
      document.getElementById('btnEsri').classList.add('active');
    }} else if (type === 'google') {{
      activeTileLayer = layerGoogle;
      currentCoordSys = 'wgs84';
      document.getElementById('btnGoogle').classList.add('active');
    }}
    map.addLayer(activeTileLayer);

    // If coordinate system changed, smoothly reposition markers
    if (oldCoordSys !== currentCoordSys) {{
      updateMarkersCoordSystem();
    }}
  }}

  // 4. Village Markers Management
  let markersList = [];
  function updateMarkersCoordSystem() {{
    markersList.forEach(mObj => {{
      const v = mObj.village;
      const targetLat = currentCoordSys === 'gcj02' ? v.gcj_lat : v.lat;
      const targetLon = currentCoordSys === 'gcj02' ? v.gcj_lon : v.lon;
      mObj.marker.setLatLng([targetLat, targetLon]);
    }});
  }}

  const townGroups = {{}};
  villagesData.forEach(v => {{ if (!townGroups[v.town]) townGroups[v.town] = []; townGroups[v.town].push(v); }});

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
        li.innerHTML = `<span>${{v.village}}</span><span class="village-tag">免翻墙</span>`;
        li.onclick = () => {{ selectVillage(v); if (isMobile) closeMobileDrawer(); }};
        ul.appendChild(li);

        if (!isMobile) {{
          const lat = currentCoordSys === 'gcj02' ? v.gcj_lat : v.lat;
          const lon = currentCoordSys === 'gcj02' ? v.gcj_lon : v.lon;
          const marker = L.circleMarker([lat, lon], {{ radius: 6, fillColor: '#2563eb', color: '#fff', weight: 2, fillOpacity: 0.85 }}).addTo(map);
          marker.bindTooltip(`<b>${{v.town}} · ${{v.village}}</b>`, {{ direction: 'top', offset: [0, -8] }});
          marker.on('click', () => selectVillage(v));
          markersList.push({{ marker, village: v }});
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
      if (el.dataset.name === v.village && el.dataset.town === v.town) el.classList.add('active');
      else el.classList.remove('active');
    }});

    const targetLat = currentCoordSys === 'gcj02' ? v.gcj_lat : v.lat;
    const targetLon = currentCoordSys === 'gcj02' ? v.gcj_lon : v.lon;
    map.flyTo([targetLat, targetLon], 18, {{ duration: 1.2 }});

    document.getElementById('cardTitle').innerText = `${{v.town}} · ${{v.village}}`;
    document.getElementById('cardCoord').innerText = `坐标：北纬 ${{v.lat.toFixed(5)}}°, 东经 ${{v.lon.toFixed(5)}}°`;
    document.getElementById('cardDesc').innerText = v.desc || '传统水乡村落，自建房集中连片区域。';
  }}

  document.querySelectorAll('.search-input').forEach(input => {{
    input.addEventListener('input', function(e) {{
      const val = e.target.value.trim().toLowerCase();
      document.querySelectorAll('.village-item').forEach(li => {{
        const name = li.dataset.name.toLowerCase();
        const town = li.dataset.town.toLowerCase();
        li.style.display = (!val || name.includes(val) || town.includes(val)) ? 'flex' : 'none';
      }});
    }});
  }});

  function openMobileDrawer() {{
    document.getElementById('drawerOverlay').style.display = 'block';
    const d = document.getElementById('mobileDrawer'); d.style.display = 'flex';
    setTimeout(() => d.classList.add('open'), 10);
  }}
  function closeMobileDrawer() {{
    const d = document.getElementById('mobileDrawer'); d.classList.remove('open');
    setTimeout(() => {{ d.style.display = 'none'; document.getElementById('drawerOverlay').style.display = 'none'; }}, 300);
  }}

  let userMarker = null;
  function locateUser() {{
    if (!navigator.geolocation) return alert('设备不支持 GPS');
    navigator.geolocation.getCurrentPosition(pos => {{
      let lat = pos.coords.latitude, lng = pos.coords.longitude;
      // If current layer is Amap (GCJ-02), convert user WGS GPS to GCJ-02
      if (currentCoordSys === 'gcj02') {{
        const gcj = wgs84ToGcj02(lat, lng);
        lat = gcj[0]; lng = gcj[1];
      }}
      map.flyTo([lat, lng], 18, {{ duration: 1.5 }});
      if (userMarker) map.removeLayer(userMarker);
      userMarker = L.circleMarker([lat, lng], {{ radius: 9, fillColor: '#ef4444', color: '#fff', weight: 3, fillOpacity: 0.9 }}).addTo(map);
      userMarker.bindPopup('<b>您当前所在的现场位置</b>').openPopup();
    }}, err => alert('无法获取位置，请在手机上允许浏览器使用位置权限。'), {{ enableHighAccuracy: true }});
  }}

  let measureMode = null, measurePoints = [], measureLine = null, measurePolygon = null, measureMarkers = [];
  function toggleMeasure(mode) {{
    clearMeasurements();
    if (measureMode === mode) {{ measureMode = null; document.getElementById('measure-info').style.display = 'none'; return; }}
    measureMode = mode;
    document.getElementById('measure-info').innerText = mode === 'distance' ? '请点击两点或多点测房距' : '请点击各拐点测面积';
    document.getElementById('measure-info').style.display = 'block';
  }}
  map.on('click', function(e) {{
    if (!measureMode) return;
    measurePoints.push(e.latlng);
    const m = L.circleMarker(e.latlng, {{ radius: 5, color: '#ef4444', fillColor: '#fff', fillOpacity: 1 }}).addTo(map);
    measureMarkers.push(m);
    if (measureMode === 'distance' && measurePoints.length >= 2) {{
      if (measureLine) map.removeLayer(measureLine);
      measureLine = L.polyline(measurePoints, {{ color: '#ef4444', weight: 3, dashArray: '6, 6' }}).addTo(map);
      let dist = 0; for (let i = 0; i < measurePoints.length - 1; i++) dist += measurePoints[i].distanceTo(measurePoints[i+1]);
      document.getElementById('measure-info').innerText = `测距：${{dist.toFixed(1)}} 米`;
    }} else if (measureMode === 'area' && measurePoints.length >= 3) {{
      if (measurePolygon) map.removeLayer(measurePolygon);
      measurePolygon = L.polygon(measurePoints, {{ color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.25 }}).addTo(map);
      const area = calcPolygonArea(measurePoints);
      document.getElementById('measure-info').innerText = `面积约：${{area.toFixed(1)}} ㎡ (${{(area * 0.0015).toFixed(2)}} 亩)`;
    }}
  }});
  function clearMeasurements() {{
    measurePoints = [];
    if (measureLine) map.removeLayer(measureLine);
    if (measurePolygon) map.removeLayer(measurePolygon);
    measureMarkers.forEach(m => map.removeLayer(m));
    measureMarkers = [];
    document.getElementById('measure-info').style.display = 'none';
  }}
  function calcPolygonArea(latlngs) {{
    const radius = 6378137; let area = 0; const len = latlngs.length;
    if (len < 3) return 0;
    for (let i = 0; i < len; i++) {{
      const p1 = latlngs[i], p2 = latlngs[(i + 1) % len];
      area += ((p2.lng - p1.lng) * (Math.PI / 180)) * (2 + Math.sin(p1.lat * (Math.PI / 180)) + Math.sin(p2.lat * (Math.PI / 180)));
    }}
    return Math.abs(area * radius * radius / 2.0);
  }}
</script>
</body>
</html>
'''
    index_file = os.path.join(web_dir, 'index.html')
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    local_file = 'd:/SynologyDrive/010-PROJECTS/美丽乡村项目/相城区村落实景规划图集/相城区村落实景数字地图.html'
    with open(local_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print('Generated China-friendly index.html successfully')

if __name__ == '__main__':
    build_china_friendly_web()
