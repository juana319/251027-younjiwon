import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정 (중앙 정렬 유지)
st.set_page_config(page_title="모눈종이 최단 경로 시뮬레이터", layout="centered")

st.markdown('<h1 style="text-align: center; color: #333; font-family: \'Noto Sans KR\', sans-serif;">🗺️ 모눈 종이 최단 경로 시뮬레이터</h1>', unsafe_allow_html=True)

# UI 개선된 조작 방식 안내 (표 디자인 및 너비 조정)
st.markdown("""
<style>
    /* 표 디자인 및 너비 조정 */
    .instruction-table {
        width: 90%; 
        max-width: 700px;
        margin: 20px auto; /* 중앙 정렬 */
        border-collapse: collapse;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-radius: 8px;
        overflow: hidden; 
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 14px; 
    }
    .instruction-table th, .instruction-table td {
        padding: 10px 12px; 
        text-align: center; 
        border: 1px solid #ddd;
        white-space: nowrap; /* 두 줄 방지 */
    }
    .instruction-table th {
        background-color: #4a90e2; 
        color: white;
        font-weight: bold;
    }
    .instruction-table tr:nth-child(even) {
        background-color: #f9f9f9; 
    }
    .instruction-table tr:hover {
        background-color: #f1f1f1; 
    }
</style>
<table class="instruction-table">
<thead>
<tr>
    <th>기능</th>
    <th>조작</th>
    <th>색상</th>
</tr>
</thead>
<tbody>
<tr>
    <td>👣 **필수 지점 (A, B, C...)**</td>
    <td>**좌클릭**</td>
    <td><span style="color:#ff6347">빨강(A)</span> / <span style="color:#4a90e2">파랑(B)</span> / <span style="color:#ffbf00">노랑(경유지)</span></td>
</tr>
<tr>
    <td>🚫 **점 장애물**</td>
    <td>**Ctrl + 좌클릭**</td>
    <td><span style="color:#2ecc71">초록색 (점)</span></td>
</tr>
<tr>
    <td>⛔ **선 장애물**</td>
    <td>**우클릭**</td>
    <td><span style="color:#2ecc71">초록색 (선)</span></td>
</tr>
<tr>
    <td>⭐ **필수 선 통과**</td>
    <td>**Ctrl + 우클릭**</td>
    <td><span style="color:#ffbf00">노란색 (선)</span></td>
</tr>
</tbody>
</table>
""", unsafe_allow_html=True)


html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  body {
    font-family: "Noto Sans KR", sans-serif;
    background: #f6f8fb;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* 전체 콘텐츠를 감싸는 파스텔 배경 컨테이너 */
  #main-container {
    background-color: #e0f7ff; /* 파스텔 하늘색 */
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    align-items: center; /* 내부 요소 중앙 정렬 */
    width: 95%; 
    max-width: 900px;
  }

  .controls { 
    margin-bottom: 25px; 
    display: flex; 
    flex-wrap: wrap; 
    justify-content: center; /* 내부 중앙 정렬 */
    gap: 15px; /* 간격 확대 */
    width: 100%; /* 컨테이너 내에서 너비 100% 사용 */
    padding: 15px;
    border-radius: 12px;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
}
  button { 
    margin: 0; 
    padding: 14px 28px; /* 버튼 크기 확대 */
    font-size: 16px; 
    cursor: pointer; 
    border: none; 
    border-radius: 20px; 
    color: white; 
    transition: all 0.2s; 
    white-space: nowrap; 
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  /* 버튼 색상 정의 */
  .btn-blue { background-color: #4a90e2; }
  .btn-red { background-color: #e74c3c; }
  .btn-yellow { background-color: #f1c40f; color: #333 !important; }

  button:hover { 
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
  .btn-blue:hover { background-color: #357ab8; }
  .btn-red:hover { background-color: #c0392b; }
  .btn-yellow:hover { background-color: #f39c12; }

  #canvas { 
    border: 1px solid #ddd; 
    background-color: white; 
    margin-bottom: 20px; 
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
}
  #result { 
    margin: 15px; 
    font-weight: bold; 
    font-size: 1.1em;
    color: #333;
    padding: 10px 20px;
    border: 2px solid #ff6347;
    border-radius: 8px;
    background: #fff0f0;
    text-align: center;
    width: 80%;
}
  #examples { 
    width: 100%; 
    display: flex; 
    flex-direction: row; 
    flex-wrap: wrap; 
    gap: 15px; 
    justify-content: center; 
    padding: 10px;
    margin-top: 10px;
  }
  .path-example { 
    border: 1px solid #ccc; 
    background: #fff; 
    padding: 5px; 
    box-sizing: border-box; 
    border-radius: 6px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
  .path-info { 
    width: 100%; 
    text-align: center; 
    font-size: 16px; 
    margin: 15px 0 10px 0;
    color: #555;
    font-weight: bold;
}
  .option-group { 
    border: 1px solid #99d6ff; /* 하늘색 계열 테두리 */
    padding: 12px 20px; 
    border-radius: 25px; 
    background: #cceeff; /* 옵션 그룹 배경색 */
    display: flex; 
    align-items: center; 
    justify-content: center;
    gap: 20px; 
    white-space: nowrap;
}
.option-group label {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    font-size: 16px; 
    color: #1c536e;
}
</style>
</head>
<body>
<div id="main-container">

  <div class="controls">
    <div class="option-group">
        <label for="reuse_yes">
            <input type="radio" id="reuse_yes" name="edge_reuse" value="yes" checked> 
            다시 지날 수 있음
        </label>
        <label for="reuse_no">
            <input type="radio" id="reuse_no" name="edge_reuse" value="no"> 
            다시 지날 수 없음
        </label>
    </div>
    <button id="calculate" class="btn-blue">경우의 수 구하기</button>
    <button id="show" class="btn-blue">사례 보기</button>
    <button id="init" class="btn-red">초기화</button>
    <button id="grid3" class="btn-yellow">3x3 설정</button>
    <button id="grid4" class="btn-yellow">4x4 설정</button>
    <button id="grid5" class="btn-yellow">5x5 설정</button>
  </div>
  <canvas id="canvas" width="420" height="420"></canvas>
  <div id="result"></div>
  <div id="examples"></div>

</div> <script>
let n = 4;
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let points = {};
let nodeObstacles = {};  
let edgeObstacles = {}; 
let mandatoryEdges = {}; 
let clickOrder = []; 
let pathOrder = []; 
let gap = 80;
const MAX_EXAMPLES_TO_DISPLAY = 500; 
const MAX_PATHS_FOR_VISUALIZATION = 100000;

function coordToKey(x, y) { return `${x},${y}`; }

function edgeToKey(x1, y1, x2, y2) {
    const k1 = coordToKey(x1, y1);
    const k2 = coordToKey(x2, y2);
    return k1 < k2 ? `${k1}-${k2}` : `${k2}-${k1}`;
}

function isNodeObstacle(x, y) { return nodeObstacles[coordToKey(x, y)] !== undefined; }
function isEdgeBlocked(x1, y1, x2, y2) { return edgeObstacles[edgeToKey(x1, y1, x2, y2)] !== undefined; }
function isEdgeMandatory(x1, y1, x2, y2) { return mandatoryEdges[edgeToKey(x1, y1, x2, y2)] !== undefined; }

function getPointColor(key) {
    if (key === "A") return "#ff6347"; // 빨강
    if (key === "B") return "#4a90e2"; // 파랑
    return "#ffbf00"; // 노랑 (경유지 C, D...)
}


function updatePathOrder() {
    pathOrder = [];
    if (points.A) pathOrder.push("A");
    for (let i = 0; i < clickOrder.length; i++) {
        const key = clickOrder[i];
        if (key !== "A" && key !== "B") {
          pathOrder.push(key);
        }
    }
    if (points.B) pathOrder.push("B");
}

function drawGrid() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.strokeStyle = "#aaa";
  ctx.lineWidth = 1;
  // 모눈선 그리기
  for (let i = 0; i <= n; i++) {
    ctx.beginPath(); ctx.moveTo(40, 40 + i*gap); ctx.lineTo(40 + n*gap, 40 + i*gap); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(40 + i*gap, 40); ctx.lineTo(40 + i*gap, 40 + n*gap); ctx.stroke();
  }
  
  // **선(간선) 그리기 (필수 선 먼저)**
  for (const key in mandatoryEdges) {
      const [k1, k2] = key.split('-');
      const [x1, y1] = k1.split(',').map(Number);
      const [x2, y2] = k2.split(',').map(Number);
      
      const cx1 = 40 + x1 * gap;
      const cy1 = 40 + y1 * gap;
      const cx2 = 40 + x2 * gap;
      const cy2 = 40 + y2 * gap;

      ctx.beginPath();
      ctx.moveTo(cx1, cy1);
      ctx.lineTo(cx2, cy2);
      ctx.strokeStyle = "#ffbf00"; // 노란색
      ctx.lineWidth = 5; 
      ctx.stroke();

      // 필수 선 표시 (★)
      const midX = (cx1 + cx2) / 2;
      const midY = (cy1 + cy2) / 2;
      ctx.fillStyle = "#333"; 
      ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; 
      ctx.fillText("★", midX, midY + 1);
  }

  // **선(간선) 장애물 그리기 (초록색)**
  for (const key in edgeObstacles) {
      const [k1, k2] = key.split('-');
      const [x1, y1] = k1.split(',').map(Number);
      const [x2, y2] = k2.split(',').map(Number);
      
      const cx1 = 40 + x1 * gap;
      const cy1 = 40 + y1 * gap;
      const cx2 = 40 + x2 * gap;
      const cy2 = 40 + y2 * gap;

      ctx.beginPath();
      ctx.moveTo(cx1, cy1);
      ctx.lineTo(cx2, cy2);
      ctx.strokeStyle = "#2ecc71"; // 초록색
      ctx.lineWidth = 5; 
      ctx.stroke();

      // 장애물 표시 (X)
      const midX = (cx1 + cx2) / 2;
      const midY = (cy1 + cy2) / 2;
      ctx.fillStyle = "white"; 
      ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("X", midX, midY);
  }

  // 점 장애물(O) 그리기
  for (const key in nodeObstacles) {
      const [x, y] = key.split(',').map(Number);
      ctx.beginPath(); ctx.arc(40 + x*gap, 40 + y*gap, 8, 0, Math.PI*2); ctx.fillStyle = "#2ecc71"; ctx.fill(); // 초록색
      ctx.fillStyle = "white"; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("O", 40 + x*gap, 40 + y*gap);
  }

  // 필수 지점 (A, B, C...) 그리기
  for (const [key, {x, y}] of Object.entries(points)) {
    ctx.beginPath(); ctx.arc(40 + x*gap, 40 + y*gap, 8, 0, Math.PI*2);
    ctx.fillStyle = getPointColor(key); ctx.fill();
    ctx.fillStyle = "white"; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(key, 40 + x*gap, 40 + y*gap);
  }
}

canvas.addEventListener("click", (e)=>{
  const rect = canvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;
  const x = Math.round((mouseX - 40)/gap);
  const y = Math.round((mouseY - 40)/gap);
  if (x < 0 || x > n || y < 0 || y > n) return;

    if (e.ctrlKey) {
        // **Ctrl + 좌클릭: 점(노드) 장애물 설정/해제 (초록색)**
        const key = coordToKey(x, y);

        for(const [k, p] of Object.entries(points)){
            if(p.x === x && p.y === y){ return; } 
        }

        if (isNodeObstacle(x, y)) { delete nodeObstacles[key]; } else { nodeObstacles[key] = {x, y}; }
        
    } else {
        // **일반 좌클릭: 점(노드) 지정 (A, B, C...)**
        if (isNodeObstacle(x, y)) return; 

        let label;
        if (!points.A) { label = "A"; } else if (!points.B) { label = "B"; } else {
            let i = 0;
            clickOrder.forEach(k => { if (k !== "A" && k !== "B") i++; });
            label = String.fromCharCode(67 + i); 
            if (i >= 24) return; 
        }

        for(const [k, p] of Object.entries(points)){
            if(p.x === x && p.y === y && k !== label){
                delete points[k];
                clickOrder = clickOrder.filter(item => item !== k);
            }
        }

        points[label] = {x, y};
        if (!clickOrder.includes(label)) { 
             if (label === "A") {
                clickOrder.unshift(label); 
            } else if (label === "B") {
                clickOrder.push(label); 
            } else {
                let insertIndex = clickOrder.length;
                if (points.B) {
                    insertIndex = clickOrder.indexOf('B');
                    if (insertIndex === -1) insertIndex = clickOrder.length;
                }
                clickOrder.splice(insertIndex, 0, label); 
            }
        }
        updatePathOrder();
    }

  drawGrid();
});

canvas.addEventListener("contextmenu", (e)=>{
    e.preventDefault(); 
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const x_approx = Math.round((mouseX - 40) / gap);
    const y_approx = Math.round((mouseY - 40) / gap);
    
    const nearestEdges = [];

    // 1. 수평 간선
    const diffY_H = Math.abs(mouseY - (40 + y_approx * gap));
    if (diffY_H < gap / 2) { 
        const diffX_H1 = Math.abs(mouseX - (40 + (x_approx - 0.5) * gap));
        if (x_approx > 0) {
             nearestEdges.push({ x1: x_approx - 1, y1: y_approx, x2: x_approx, y2: y_approx, dist: Math.hypot(diffX_H1, diffY_H) });
        }
        const diffX_H2 = Math.abs(mouseX - (40 + (x_approx + 0.5) * gap));
        if (x_approx < n) {
             nearestEdges.push({ x1: x_approx, y1: y_approx, x2: x_approx + 1, y2: y_approx, dist: Math.hypot(diffX_H2, diffY_H) });
        }
    }

    // 2. 수직 간선
    const diffX_V = Math.abs(mouseX - (40 + x_approx * gap));
     if (diffX_V < gap / 2) { 
        const diffY_V1 = Math.abs(mouseY - (40 + (y_approx - 0.5) * gap));
         if (y_approx > 0) {
             nearestEdges.push({ x1: x_approx, y1: y_approx - 1, x2: x_approx, y2: y_approx, dist: Math.hypot(diffX_V, diffY_V1) });
        }
        const diffY_V2 = Math.abs(mouseY - (40 + (y_approx + 0.5) * gap));
        if (y_approx < n) {
             nearestEdges.push({ x1: x_approx, y1: y_approx, x2: x_approx, y2: y_approx + 1, dist: Math.hypot(diffX_V, diffY_V2) });
        }
    }
    
    if (nearestEdges.length > 0) {
        nearestEdges.sort((a, b) => a.dist - b.dist);
        const targetEdge = nearestEdges[0];
        const edgeKey = edgeToKey(targetEdge.x1, targetEdge.y1, targetEdge.x2, targetEdge.y2);
        
        const isPointOnEdge = Object.values(points).some(p => 
            (p.x === targetEdge.x1 && p.y === targetEdge.y1) || 
            (p.x === targetEdge.x2 && p.y === targetEdge.y2)
        );

        if (!isPointOnEdge) {
            if (e.ctrlKey) {
                // **Ctrl + 우클릭: 필수 선(간선) 통과 설정/해제 (노란색)**
                if (isEdgeBlocked(targetEdge.x1, targetEdge.x1, targetEdge.x2, targetEdge.y2)) {
                } else if (isEdgeMandatory(targetEdge.x1, targetEdge.y1, targetEdge.x2, targetEdge.y2)) {
                    delete mandatoryEdges[edgeKey];
                } else {
                    mandatoryEdges[edgeKey] = true;
                }

            } else {
                // **일반 우클릭: 선(간선) 장애물 설정/해제 (초록색)**
                if (isEdgeMandatory(targetEdge.x1, targetEdge.y1, targetEdge.x2, targetEdge.y2)) {
                } else if (isEdgeBlocked(targetEdge.x1, targetEdge.y1, targetEdge.x2, targetEdge.y2)) {
                    delete edgeObstacles[edgeKey];
                } else {
                    edgeObstacles[edgeKey] = true;
                }
            }
        }
    }

  drawGrid();
});

// 이 함수는 이제 calculateTotalPaths에서 사용되지 않지만, 다른 곳에서 사용될 경우를 대비해 유지합니다.
function comb(n,r){ 
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  if (r > n / 2) r = n - r; 

  let res = 1;
  for (let i = 1; i <= r; i++) {
    res = res * (n - i + 1) / i;
  }
  return Math.round(res); 
}

// 이 함수는 이제 calculateTotalPaths에서 사용되지 않지만, 다른 곳에서 사용될 경우를 대비해 유지합니다.
function pathCountWithNodeObstacles(p1, p2, obstacleList){
    const dx = Math.abs(p2.x - p1.x); 
    const dy = Math.abs(p2.y - p1.y); 

    if (p2.x < p1.x || p2.y < p1.y) return 0;

    let totalPaths = comb(dx + dy, dx); 

    const relevantObstacles = obstacleList.filter(o => {
        return o.x >= p1.x && o.x <= p2.x && o.y >= p1.y && o.y <= p2.y;
    });
    
    if (relevantObstacles.length === 0) return totalPaths;

    let finalCount = totalPaths;
    relevantObstacles.sort((a, b) => (a.x + a.y) - (b.x + b.y));

    for (let count = 1; count <= relevantObstacles.length; count++) {
        let combinationSum = 0;
        const indices = new Array(count).fill(0).map((_, i) => i);

        let done = false;
        while (!done) {
            const currentObstacles = indices.map(i => relevantObstacles[i]);
            let pathProduct = 1;
            const pointsToCalculate = [p1, ...currentObstacles, p2];

            for (let i = 0; i < pointsToCalculate.length - 1; i++) {
                const start = pointsToCalculate[i];
                const end = pointsToCalculate[i+1];
                const segmentDx = Math.abs(end.x - start.x);
                const segmentDy = Math.abs(end.y - start.y);
                if (end.x < start.x || end.y < start.y) { pathProduct = 0; break; }
                pathProduct *= comb(segmentDx + segmentDy, segmentDx);
            }
            
            combinationSum += pathProduct;

            let k = indices.length - 1;
            while (k >= 0 && indices[k] === relevantObstacles.length - count + k) { k--; }
            if (k < 0) {
                done = true;
            } else {
                indices[k]++;
                for (let j = k + 1; j < indices.length; j++) {
                    indices[j] = indices[j - 1] + 1;
                }
            }
        } 
        if (count % 2 === 1) { finalCount -= combinationSum; } else { finalCount += combinationSum; }
    }
    
    return finalCount < 0 ? 0 : finalCount; 
}


function calculateTotalPaths(allowEdgeReuse){
    if(pathOrder.length < 2) return 0;
    
    // 사용자 요청에 따라, 무조건 탐색 기반으로 경로 수를 계산하여 반환합니다.
    const paths = generatePaths(allowEdgeReuse);
    return paths.length; // 경로 수만 반환
}


document.getElementById("calculate").addEventListener("click", ()=>{
  const allowEdgeReuse = document.getElementById('reuse_yes').checked;
  const total = calculateTotalPaths(allowEdgeReuse);

  // 탐색 기반으로 계산된 총 경로 수 표시 (사례 개수와 일치)
  if (total === 0) {
      document.getElementById("result").textContent=`총 최단거리 경로 수: 0 가지 (경로 불가)`;
  } else if (total > MAX_PATHS_FOR_VISUALIZATION) {  
      document.getElementById("result").textContent=`총 최단거리 경로 수: ${total} 가지 (계산됨, 시각화는 제한)`;
  } else { 
      document.getElementById("result").textContent=`총 최단거리 경로 수: ${total} 가지`;
  }
});


function generatePaths(allowEdgeReuse){
  const allPaths = [];
  let currentTotalPaths = 1;
  
  for(let i=0;i<pathOrder.length-1;i++){
    const p1 = points[pathOrder[i]];
    const p2 = points[pathOrder[i+1]];
    const segmentPaths = [];

    const requiredLength = Math.abs(p2.x - p1.x) + Math.abs(p2.y - p1.y);
    
    const segmentMandatoryEdges = new Set();
    for (const key in mandatoryEdges) {
        const [k1, k2] = key.split('-');
        const [x1, y1] = k1.split(',').map(Number);
        const [x2, y2] = k2.split(',').map(Number);

        const minX = Math.min(p1.x, p2.x);
        const maxX = Math.max(p1.x, p2.x);
        const minY = Math.min(p1.y, p2.y);
        const maxY = Math.max(p1.y, p2.y);

        if ((x1 >= minX && x1 <= maxX && y1 >= minY && y1 <= maxY) &&
            (x2 >= minX && x2 <= maxX && y2 >= minY && y2 <= maxY)) {
            segmentMandatoryEdges.add(key);
        }
    }


    function dfs(x,y,path, currentEdges){
      if (currentTotalPaths > MAX_PATHS_FOR_VISUALIZATION) return; 
      if (isNodeObstacle(x, y)) return; 
      if (path.length > requiredLength) return; 
      
      if(x===p2.x && y===p2.y){ 
        if (path.length === requiredLength) { 
            let hasAllMandatory = true;
            for (const key of segmentMandatoryEdges) {
                if (!currentEdges.has(key)) {
                    hasAllMandatory = false;
                    break;
                }
            }

            if (hasAllMandatory) {
                segmentPaths.push({path: [...path], edges: new Set(currentEdges)});
            }
        }
        return; 
      }
      
      const directions = [];
      if(x<p2.x) directions.push({dx: 1, dy: 0, dir: "R"}); 
      if(p2.y >= p1.y && y<p2.y) directions.push({dx: 0, dy: 1, dir: "D"}); 
      if(p2.y < p1.y && y>p2.y) directions.push({dx: 0, dy: -1, dir: "U"}); 

      
      for(const {dx, dy, dir} of directions){
          const nextX = x + dx;
          const nextY = y + dy;
            const edgeKey = edgeToKey(x, y, nextX, nextY);

            if (isEdgeBlocked(x, y, nextX, nextY)) {
                continue; 
            }
          
            const nextEdges = new Set(currentEdges);
            nextEdges.add(edgeKey);
          
            dfs(nextX, nextY, [...path, dir], nextEdges);
      }
    }
    
    if (isNodeObstacle(p1.x, p1.y)) return []; 
    
    dfs(p1.x,p1.y,[], new Set());
    
    if (segmentPaths.length === 0) return [];
    
    allPaths.push(segmentPaths);
    
    currentTotalPaths *= segmentPaths.length;
    if (currentTotalPaths > MAX_PATHS_FOR_VISUALIZATION) break;
  }
  
  if (allPaths.length === 0) return [];
  
  let finalPaths = allPaths[0].map(item => ({path: item.path, edges: item.edges}));
  
  for (let i = 1; i < allPaths.length; i++) {
    const nextSegmentPaths = allPaths[i];
    const newFinalPaths = [];
    
    for (const item of finalPaths) {
      for (const nextItem of nextSegmentPaths) {
        if (newFinalPaths.length >= MAX_EXAMPLES_TO_DISPLAY) break;
        
        let isSimplePath = true;
        const newEdges = new Set(item.edges);

        for (const key of nextItem.edges) {
             if (!allowEdgeReuse && item.edges.has(key)) {
                 isSimplePath = false;
                 break;
             }
             newEdges.add(key);
        }

        if (allowEdgeReuse || isSimplePath) { 
          newFinalPaths.push({
              path: [...item.path, ...nextItem.path],
              edges: newEdges 
          });
        }
      }
      if (newFinalPaths.length >= MAX_EXAMPLES_TO_DISPLAY) break;
    }
    finalPaths = newFinalPaths;
    if (finalPaths.length === 0) return [];
  }

  return finalPaths.map(item => item.path);
}

document.getElementById("show").addEventListener("click", ()=>{
  const allowEdgeReuse = document.getElementById('reuse_yes').checked;
  const exDiv=document.getElementById("examples");
  exDiv.innerHTML="";
  
  if(pathOrder.length < 2){ exDiv.textContent="최소 두 지점(A와 B)을 먼저 지정하세요."; return; }
  
  const paths=generatePaths(allowEdgeReuse);
  const totalPathsCount = paths.length;
  const numToDisplay = Math.min(totalPathsCount, MAX_EXAMPLES_TO_DISPLAY);


  const infoDiv=document.createElement("div");
  infoDiv.className="path-info";
  
  if (totalPathsCount === 0) {
      infoDiv.textContent = "조건을 만족하는 최단 경로가 없습니다.";
      exDiv.appendChild(infoDiv);
      return;
  }
  
  // 간소화된 메시지: 총 [사례 개수]가지 사례를 표시합니다.
  infoDiv.textContent=`총 ${numToDisplay}가지 사례를 표시합니다.`; 
  exDiv.appendChild(infoDiv);


  // 시각화 로직
  const allX = pathOrder.map(key => points[key].x);
  const allY = pathOrder.map(key => points[key].y);
  const minX = Math.min(...allX, ...Object.values(nodeObstacles).map(p=>p.x), ...Object.keys(edgeObstacles).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[0]))), ...Object.keys(mandatoryEdges).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[0]))));
  const minY = Math.min(...allY, ...Object.values(nodeObstacles).map(p=>p.y), ...Object.keys(edgeObstacles).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[1]))), ...Object.keys(mandatoryEdges).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[1]))));
  const maxX = Math.max(...allX, ...Object.values(nodeObstacles).map(p=>p.x), ...Object.keys(edgeObstacles).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[0]))), ...Object.keys(mandatoryEdges).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[0]))));
  const maxY = Math.max(...allY, ...Object.values(nodeObstacles).map(p=>p.y), ...Object.keys(edgeObstacles).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[1]))), ...Object.keys(mandatoryEdges).flatMap(k=>k.split('-').map(c=>Number(c.split(',')[1]))));


  const totalDx = maxX - minX;
  const totalDy = maxY - minY;

  const scale=25; 
  const maxMiniSize = 250; 
  const canvasWidth = 10 + (totalDx+1) * scale + 10;
  const canvasHeight = 10 + (totalDy+1) * scale + 10;
  let skippedCount = 0;


  paths.slice(0, numToDisplay).forEach((path,i)=>{
    const mini=document.createElement("canvas");
    
    // 크기가 너무 크면 스킵하여 레이아웃 유지
    if (canvasWidth > maxMiniSize || canvasHeight > maxMiniSize) { skippedCount++; return; }
    mini.width = canvasWidth; mini.height = canvasHeight;
    const c=mini.getContext("2d");
    
    c.strokeStyle="#eee"; c.lineWidth = 1;
    for(let j=0;j<=totalDy;j++){ c.beginPath(); c.moveTo(10,10+j*scale); c.lineTo(10+(totalDx)*scale,10+j*scale); c.stroke(); }
    for(let j=0;j<=totalDx;j++){ c.beginPath(); c.moveTo(10+j*scale,10); c.lineTo(10+j*scale,10+(totalDy)*scale); c.stroke(); }
    
    // **선 조건 미니맵에도 그리기 (필수 선 우선)**
    for (const [key, isMandatory] of Object.entries({...edgeObstacles, ...mandatoryEdges})) {
        const [k1, k2] = key.split('-');
        const [x1, y1] = k1.split(',').map(Number);
        const [x2, y2] = k2.split(',').map(Number);
        
        const cx1 = 10 + (x1 - minX) * scale;
        const cy1 = 10 + (y1 - minY) * scale;
        const cx2 = 10 + (x2 - minX) * scale;
        const cy2 = 10 + (y2 - minY) * scale;

        if (cx1 < -scale || cx2 > mini.width + scale || cy1 < -scale || cy2 > mini.height + scale) continue;

        c.beginPath();
        c.moveTo(cx1, cy1);
        c.lineTo(cx2, cy2);
        c.strokeStyle = mandatoryEdges[key] ? "#ffbf00" : "#2ecc71"; // 노랑/초록
        c.lineWidth = 3; 
        c.stroke();
    }


    let cx = 10 + (points.A.x - minX) * scale;
    let cy = 10 + (points.A.y - minY) * scale;
    c.beginPath(); c.moveTo(cx,cy);
    path.forEach(step=>{
      if(step==="R") cx+=scale; else if(step==="D") cy+=scale; else if(step==="U") cy-=scale;
      c.lineTo(cx,cy); 
    });
    c.strokeStyle="#ff6347"; c.lineWidth=2; c.stroke(); 
    
    // 필수 지점 마커
    pathOrder.forEach(key => {
        const p = points[key];
        const markerX = 10 + (p.x - minX) * scale;
        const markerY = 10 + (p.y - minY) * scale;
        let color = getPointColor(key);
        c.fillStyle = color; c.beginPath(); c.arc(markerX, markerY, 4, 0, Math.PI*2); c.fill();
    });
    
    // 점 장애물 마커
    for (const key in nodeObstacles) {
        const obs = nodeObstacles[key];
        const obsX = 10 + (obs.x - minX) * scale;
        const obsY = 10 + (obs.y - minY) * scale;
        c.fillStyle = "#2ecc71"; c.beginPath(); c.arc(obsX, obsY, 4, 0, Math.PI*2); c.fill();
    }


    const div=document.createElement("div");
    div.className="path-example";
    div.appendChild(mini);
    exDiv.appendChild(div);
  });
  
  if (skippedCount > 0) {
     exDiv.innerHTML += `<p style='width: 100%; text-align: center; color: #e74c3c;'>* 모눈 크기가 너무 커서 ${skippedCount}개 사례의 시각화가 생략되었습니다. *</p>`;
  }
});

document.getElementById("init").addEventListener("click", ()=>{
  points={}; clickOrder=[]; pathOrder=[]; nodeObstacles={}; edgeObstacles={}; mandatoryEdges={};
  document.getElementById("result").textContent="";
  document.getElementById("examples").innerHTML="";
  document.getElementById('reuse_yes').checked = true; 
  drawGrid();
});

document.getElementById("grid3").addEventListener("click", ()=>{ n=3; gap=100; resizeCanvas(); });
document.getElementById("grid4").addEventListener("click", ()=>{ n=4; gap=80; resizeCanvas(); });
document.getElementById("grid5").addEventListener("click", ()=>{ n=5; gap=60; resizeCanvas(); });


function resizeCanvas(){
  canvas.width = 40 + n*gap + 40;
  canvas.height = 40 + n*gap + 40;
  points={}; clickOrder=[]; pathOrder=[]; nodeObstacles={}; edgeObstacles={}; mandatoryEdges={};
  document.getElementById("result").textContent="";
  document.getElementById("examples").innerHTML="";
  document.getElementById('reuse_yes').checked = true;
  drawGrid();
}

drawGrid();
</script>
</body>
</html>
"""

components.html(html_code, height=12000)