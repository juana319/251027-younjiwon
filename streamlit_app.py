import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="모눈 위 최단 경로 시각화 (A->...->B)", layout="centered")

st.title("모눈 위 최단 경로 시각화")

st.write("👣 **A**에서 출발해 **클릭한 경유지들을 순서대로** 모두 거쳐 **B**에 도착하는 최단 경로를 확인해보세요!")
st.markdown("**(클릭 순서: A $\to$ B $\to$ C $\to$ D... 이 경우 경로는 A $\to$ C $\to$ D $\to$ B 가 됩니다)**")

# HTML + JS 코드
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
  .controls {
    margin-bottom: 10px;
  }
  button {
    margin: 5px;
    padding: 6px 14px;
    font-size: 14px;
    cursor: pointer;
    border: none;
    border-radius: 8px;
    background-color: #4a90e2;
    color: white;
  }
  button:hover { background-color: #357ab8; }
  #canvas {
    border: 1px solid #888;
    background-color: white;
    margin-bottom: 15px;
  }
  #result { margin: 8px; font-weight: bold; }
  /* **수정된 부분: 가로 배열 유지 + 줄 바꿈 (flex-wrap: wrap)** */
  #examples { 
    display: flex; 
    flex-direction: row; /* 가로 방향으로 요소들을 배치 */
    flex-wrap: wrap; /* 요소들이 넘칠 경우 다음 줄로 내려가게 함 (배열 깨짐 방지) */
    gap: 15px; /* 항목 간 간격 */
    justify-content: center; /* 중앙 정렬 */
    width: 100%; /* 너비 꽉 채움 */
    padding: 10px;
  }
  .path-example {
    border: 1px solid #ccc;
    background: #fff;
    padding: 5px;
    /* 사례 크기 조정이 용이하도록 너비를 제한 (필요시 조정) */
    box-sizing: border-box; 
  }
  .path-info {
      width: 100%;
      text-align: center;
      font-size: 14px;
      margin-bottom: 10px;
  }
</style>
</head>
<body>
  <div class="controls">
    <button id="init">초기화</button>
    <button id="calculate">경우의 수 구하기</button>
    <button id="show">사례보기</button>
    <button id="grid3">3×3</button>
    <button id="grid4">4×4</button>
    <button id="grid5">5×5</button>
  </div>
  <canvas id="canvas" width="420" height="420"></canvas>
  <div id="result"></div>
  <div id="examples"></div>

<script>
let n = 4; // 기본 4x4
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let points = {};
let clickOrder = []; // 클릭된 모든 점의 순서 (A, B, C, D...)
let pathOrder = []; // 실제로 경로 계산에 사용될 순서 (A, C, D..., B)
let gap = 80;
const MAX_EXAMPLES_TO_DISPLAY = 500; // 시각화 최대 개수 (총 경로가 이보다 적으면 모두 표시)
const MAX_PATH_GENERATION_LIMIT = 100000; // 경로 생성 알고리즘이 멈추는 기준

// 경로 계산에 사용할 순서 배열을 업데이트하는 함수
function updatePathOrder() {
    pathOrder = [];
    if (points.A) pathOrder.push("A");
    
    // C, D, E... (인덱스 2부터) 를 A와 B 사이에 순서대로 추가
    for (let i = 2; i < clickOrder.length; i++) {
        pathOrder.push(clickOrder[i]);
    }

    if (points.B) pathOrder.push("B");
}

function drawGrid() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.strokeStyle = "#aaa";
  ctx.lineWidth = 1;
  // 모눈선 그리기
  for (let i = 0; i <= n; i++) {
    ctx.beginPath();
    ctx.moveTo(40, 40 + i*gap);
    ctx.lineTo(40 + n*gap, 40 + i*gap);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(40 + i*gap, 40);
    ctx.lineTo(40 + i*gap, 40 + n*gap);
    ctx.stroke();
  }
  // 점 그리기
  for (const [key, {x, y}] of Object.entries(points)) {
    ctx.beginPath();
    ctx.arc(40 + x*gap, 40 + y*gap, 8, 0, Math.PI*2);
    // A는 빨강, B는 파랑, 나머지는 주황
    ctx.fillStyle = key==="A"?"#ff6f61":key==="B"?"#4a90e2":"#f5b041";
    ctx.fill();
    ctx.fillStyle = "white";
    ctx.font = "bold 12px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(key, 40 + x*gap, 40 + y*gap);
  }
}

canvas.addEventListener("click", (e)=>{
  const rect = canvas.getBoundingClientRect();
  const x = Math.round((e.clientX - rect.left - 40)/gap);
  const y = Math.round((e.clientY - rect.top - 40)/gap);
  if (x < 0 || x > n || y < 0 || y > n) return;
  
  let label;
  if (!points.A) {
    label = "A";
  } else if (!points.B) {
    label = "B";
  } else {
    // C, D, E... 순서로 추가
    let i = clickOrder.length;
    label = String.fromCharCode(65 + i); 
    if (i >= 26) return; // 너무 많은 점 방지
  }

  points[label] = {x, y};
  if (!clickOrder.includes(label)) {
    clickOrder.push(label);
  }
  updatePathOrder();
  drawGrid();
});

// 팩토리얼 함수
function factorial(num){ 
  if (num < 0) return 0;
  let result = 1;
  for (let i = 2; i <= num; i++) {
    result *= i;
  }
  return result; 
}

// 조합 함수 nCr
function comb(n,r){ 
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  if (r > n / 2) r = n - r; 

  let res = 1;
  for (let i = 1; i <= r; i++) {
    res = res * (n - i + 1) / i;
  }
  return res;
}

// 두 지점 사이의 최단 경로 개수 (같은 것을 포함하는 순열)
function pathCount(p1,p2){
  const dx=Math.abs(p1.x-p2.x);
  const dy=Math.abs(p1.y-p2.y);
  
  // p2의 좌표가 p1보다 크거나 같은 경우 (오른쪽/아래 이동)만 허용
  if (p2.x < p1.x || p2.y < p1.y) {
    return 0; 
  }
  return comb(dx+dy,dx);
}

// 모든 지점을 순서대로 지나는 최단 경로의 총 개수 계산
document.getElementById("calculate").addEventListener("click", ()=>{
  if(pathOrder.length < 2){ 
    document.getElementById("result").textContent="최소 두 지점(A와 B)을 지정하세요."; return;
  }
  let total=1;
  let pathPossible = true;

  // pathOrder 배열에 지정된 순서대로 각 구간의 경로 개수를 곱함
  for(let i=0;i<pathOrder.length-1;i++){
    const count = pathCount(points[pathOrder[i]],points[pathOrder[i+1]]);
    if (count === 0) {
      pathPossible = false;
      total = 0;
      break;
    }
    total *= count;
  }

  if (pathPossible && total > MAX_PATH_GENERATION_LIMIT) { 
      document.getElementById("result").textContent=`총 최단거리 경로 수: ${total} 가지 (경우의 수가 너무 많아 시각화는 제한됩니다)`;
  } else if (!pathPossible) {
      document.getElementById("result").textContent=`총 최단거리 경로 수: 0 가지 (지점 간의 순서가 최단 경로 조건을 만족하지 않습니다)`;
  } else {
      document.getElementById("result").textContent=`총 최단거리 경로 수: ${total} 가지`;
  }
});

// A에서 B까지 모든 중간 지점을 지나는 모든 경로 생성 (DFS 기반)
function generatePaths(){
  const allPaths = [];
  let currentTotalPaths = 1;
  
  // pathOrder에 따라 각 구간별 경로를 생성하고 결합
  for(let i=0;i<pathOrder.length-1;i++){
    const p1 = points[pathOrder[i]];
    const p2 = points[pathOrder[i+1]];
    const segmentPaths = [];

    // 최단 경로 조건 확인
    if (p2.x < p1.x || p2.y < p1.y) {
        return []; // 최단 경로 불가
    }

    function dfs(x,y,path){
      // 경로 수가 너무 많아지면 경로 생성을 중단합니다. (시각화 부담 최소화)
      if (currentTotalPaths > MAX_PATH_GENERATION_LIMIT) return; 

      if(x===p2.x && y===p2.y){ 
        segmentPaths.push([...path]);
        return; 
      }
      if(x<p2.x) dfs(x+1,y,[...path,"R"]); // Right
      if(y<p2.y) dfs(x,y+1,[...path,"D"]); // Down
    }
    dfs(p1.x,p1.y,[]);
    allPaths.push(segmentPaths);
    
    // 다음 구간으로 넘어가기 전에 현재까지의 총 경로 개수를 업데이트하고 제한 확인
    currentTotalPaths *= segmentPaths.length;
    if (currentTotalPaths > MAX_PATH_GENERATION_LIMIT) break;
  }

  // 모든 구간 경로를 결합하여 최종 경로 생성
  if (allPaths.length === 0) return [];
  
  let finalPaths = allPaths[0];

  for (let i = 1; i < allPaths.length; i++) {
    const nextSegmentPaths = allPaths[i];
    const newFinalPaths = [];
    for (const p1 of finalPaths) {
      for (const p2 of nextSegmentPaths) {
        newFinalPaths.push([...p1, ...p2]);
        // 결합 과정에서도 경로 개수가 시각화 제한을 넘으면 즉시 중단
        if (newFinalPaths.length >= MAX_EXAMPLES_TO_DISPLAY) { 
            return newFinalPaths; 
        }
      }
    }
    finalPaths = newFinalPaths;
  }

  return finalPaths;
}

// 경로 시각화
document.getElementById("show").addEventListener("click", ()=>{
  const exDiv=document.getElementById("examples");
  exDiv.innerHTML="";
  
  if(pathOrder.length < 2){ 
    exDiv.textContent="최소 두 지점(A와 B)을 먼저 지정하세요."; return;
  }
  
  const paths=generatePaths();
  const totalPathsCount = paths.length;
  const numToDisplay = Math.min(totalPathsCount, MAX_EXAMPLES_TO_DISPLAY);

  if (totalPathsCount === 0) {
      document.getElementById("result").textContent=`총 최단거리 경로 수: 0 가지 (지점 간의 순서가 최단 경로 조건을 만족하지 않습니다)`;
      exDiv.textContent="조건을 만족하는 최단 경로가 없습니다.";
      return;
  }

  // 경우의 수 안내 문구
  const pathCalcTotal = parseInt(document.getElementById("result").textContent.match(/:\s*(\d+)/)[1]);
  const infoDiv=document.createElement("div");
  infoDiv.className="path-info";
  if (pathCalcTotal > MAX_EXAMPLES_TO_DISPLAY) {
      infoDiv.textContent=`총 ${pathCalcTotal}가지 경로 중 ${numToDisplay}가지 사례를 표시합니다.`;
  } else {
      infoDiv.textContent=`총 ${totalPathsCount}가지 사례를 표시합니다.`;
  }
  exDiv.appendChild(infoDiv);


  // A에서 B까지의 전체 모눈 크기 계산 (시각화용)
  const allX = pathOrder.map(key => points[key].x);
  const allY = pathOrder.map(key => points[key].y);
  const minX = Math.min(...allX);
  const minY = Math.min(...allY);
  const maxX = Math.max(...allX);
  const maxY = Math.max(...allY);

  const totalDx = maxX - minX;
  const totalDy = maxY - minY;

  const scale=25; // 미니 캔버스 셀 크기
  const maxMiniSize = 250; // 최대 캔버스 크기 제한
  const canvasWidth = 10 + totalDx * scale + 10;
  const canvasHeight = 10 + totalDy * scale + 10;
  let skippedCount = 0;


  paths.slice(0, numToDisplay).forEach((path,i)=>{
    const mini=document.createElement("canvas");
    
    // 미니 캔버스 크기 조정
    if (canvasWidth > maxMiniSize || canvasHeight > maxMiniSize) {
        skippedCount++;
        return; 
    }
    mini.width = canvasWidth;
    mini.height = canvasHeight;
    
    const c=mini.getContext("2d");
    
    // 모눈 그리기
    c.strokeStyle="#eee"; 
    c.lineWidth = 1;
    for(let j=0;j<=totalDy;j++){
      c.beginPath();
      c.moveTo(10,10+j*scale);
      c.lineTo(10+totalDx*scale,10+j*scale);
      c.stroke();
    }
    for(let j=0;j<=totalDx;j++){
      c.beginPath();
      c.moveTo(10+j*scale,10);
      c.lineTo(10+j*scale,10+totalDy*scale);
      c.stroke();
    }
    
    // 경로 그리기
    let cx = 10 + (points.A.x - minX) * scale;
    let cy = 10 + (points.A.y - minY) * scale;
    
    c.beginPath();
    c.moveTo(cx,cy);
    
    path.forEach(step=>{
      if(step==="R") cx+=scale;
      else if(step==="D") cy+=scale;
      c.lineTo(cx,cy); // 경로 그리기
    });
    
    c.strokeStyle="#ff6f61";
    c.lineWidth=2;
    c.stroke();
    
    // 모든 지점 (경유지 포함) 마커
    pathOrder.forEach(key => {
        const p = points[key];
        const markerX = 10 + (p.x - minX) * scale;
        const markerY = 10 + (p.y - minY) * scale;
        
        let color = key==="A"?"#ff6f61":key==="B"?"#4a90e2":"#f5b041";
        
        c.fillStyle = color;
        c.beginPath();
        c.arc(markerX, markerY, 4, 0, Math.PI*2);
        c.fill();
        
        c.fillStyle = "white";
        c.font = "bold 8px sans-serif";
        c.textAlign = "center";
        c.textBaseline = "middle";
        c.fillText(key, markerX, markerY);
    });


    const div=document.createElement("div");
    div.className="path-example";
    div.appendChild(mini);
    exDiv.appendChild(div);
  });
  
  if (skippedCount > 0) {
     exDiv.innerHTML += `<p style='width: 100%; text-align: center;'>* 모눈 크기(${totalDx}x${totalDy})가 너무 커서 ${skippedCount}개 사례의 시각화가 생략되었습니다. *</p>`;
  }
});

document.getElementById("init").addEventListener("click", ()=>{
  points={}; clickOrder=[]; pathOrder=[];
  document.getElementById("result").textContent="";
  document.getElementById("examples").innerHTML="";
  drawGrid();
});

document.getElementById("grid3").addEventListener("click", ()=>{ n=3; gap=100; resizeCanvas(); });
document.getElementById("grid4").addEventListener("click", ()=>{ n=4; gap=80; resizeCanvas(); });
document.getElementById("grid5").addEventListener("click", ()=>{ n=5; gap=60; resizeCanvas(); });

function resizeCanvas(){
  canvas.width = 40 + n*gap + 40;
  canvas.height = 40 + n*gap + 40;
  points={}; clickOrder=[]; pathOrder=[];
  document.getElementById("result").textContent="";
  document.getElementById("examples").innerHTML="";
  drawGrid();
}

drawGrid();
</script>
</body>
</html>
"""

components.html(html_code, height=12000)