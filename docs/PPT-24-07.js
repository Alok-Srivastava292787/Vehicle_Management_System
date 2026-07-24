bash -lc cat > /mnt/data/create_v2_ppt.js <<'EOF'
const pptxgen=require('pptxgenjs');
const pptx=new pptxgen();
pptx.layout='LAYOUT_WIDE';
pptx.author='M365 Copilot';
pptx.company='UST';
pptx.subject='Vehicle Management System RC1';
const slides=[
['Vehicle Management System','Fleet Maintenance & Workshop Operations Platform\nRelease Candidate 1 (RC1)'],
['Business Challenges','• Manual registers and spreadsheets\n• Disconnected maintenance workflow\n• Limited auditability\n• Delayed reporting'],
['Objectives','• Digitize maintenance lifecycle\n• Improve visibility\n• Standardize processes\n• Generate operational documents'],
['Architecture','React + Vite UI\nFastAPI Services\nPostgreSQL Database\nReportLab PDF Engine'],
['Master Data Management','Vehicle Master\nDriver Master\nEmployee Master\nPart Master'],
['End-to-End Workflow','Vehicle → Complaint → Inspection → Job Card → Part Requisition → Completion'],
['Job Card Management','Maintenance execution, technicians, parts usage, approvals and PDF generation'],
['Part Requisition Workflow','Request parts, track quantities, serial numbers and requisition lifecycle'],
['Dashboard & Governance','Dashboard Metrics\nRecent Activity\nAudit Logs\nSoft Delete'],
['Reporting','Job Card PDF\nPart Requisition PDF\nReusable PDF Framework'],
['Testing Coverage','CRUD Tests\nAPI Tests\nWorkflow Validation\nPDF Validation'],
['Business Benefits','Traceability\nStandardization\nOperational Efficiency\nDigital Documentation'],
['Roadmap','Inventory Issue & Return\nStock Ledger\nNotifications\nAdvanced Analytics'],
['Thank You','Questions & Discussion']
];
slides.forEach((s,i)=>{let sl=pptx.addSlide();sl.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.33,h:0.5,fill:{color:'1F4E79'},line:{color:'1F4E79'}});sl.addText(s[0],{x:0.4,y:0.7,w:12,h:0.5,fontSize:24,bold:true,color:'1F4E79'});sl.addText(s[1],{x:0.8,y:1.5,w:11.5,h:3,fontSize:18,color:'333333'});sl.addShape(pptx.ShapeType.line,{x:0.4,y:6.8,w:12.2,h:0,line:{color:'BFBFBF',pt:1}});sl.addText('Vehicle Management System RC1 | Internal Use Only',{x:2,y:6.9,w:9,h:0.25,fontSize:8,color:'666666',align:'center'});});
pptx.writeFile({fileName:'/mnt/data/Vehicle_Management_System_RC1_V2.pptx'});
EOF
node /mnt/data/create_v2_ppt.js
