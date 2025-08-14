const fs = require('fs');
const path = require('path');

function graphToStepsWithDescription(graphPath) {
    const raw = JSON.parse(fs.readFileSync(graphPath, 'utf-8'));

    let nodes = [];
    let edges = [];

    // جدا کردن nodes و edges
    if (Array.isArray(raw)) {
        nodes = raw.filter(item => item.id);
        edges = raw.filter(item => item.source && item.target);
    } else {
        nodes = raw.nodes || [];
        edges = raw.edges || [];
    }

    let steps = [];
    let visited = new Set();
    let descriptions = [];

    function describeNode(node) {
        // توضیح انگلیسی کوتاه برای هر نود
        return `Node '${node.id}': ${node.label || "No label"} - represents a step or function in the flow.`;
    }

    function describeEdge(edge) {
        // توضیح انگلیسی کوتاه برای هر یال
        return `Edge from '${edge.source}' to '${edge.target}': indicates flow or dependency.`;
    }

    function traverse(nodeId) {
        if (visited.has(nodeId)) return;
        visited.add(nodeId);

        let node = nodes.find(n => n.id === nodeId);
        if (!node) return;

        let label = node.label || node.id || "";
        label = label.replace(/\n/g, ' ').trim();

        if (label) {
            steps.push(`${steps.length + 1}. ${label}`);
            descriptions.push(describeNode(node));
        }

        let nextEdges = edges.filter(e => e.source === nodeId);
        for (let edge of nextEdges) {
            descriptions.push(describeEdge(edge));
            traverse(edge.target);
        }
    }

    // پیدا کردن ریشه‌ها (گره‌هایی که هیچکس بهشون وصل نیست)
    let targetSet = new Set(edges.map(e => e.target));
    let rootNodes = nodes.filter(n => !targetSet.has(n.id));

    // اگر ریشه پیدا نشد، همه نودها رو بگیریم
    if (rootNodes.length === 0) rootNodes = nodes;

    for (let root of rootNodes) {
        traverse(root.id);
    }

    return {
        steps,
        descriptions
    };
}

// اجرای مستقیم
if (require.main === module) {
    const graphPath = path.resolve(__dirname, '../graphs/graph.json');
    if (!fs.existsSync(graphPath)) {
        console.error(` File not found: ${graphPath}`);
        process.exit(1);
    }

    const { steps, descriptions } = graphToStepsWithDescription(graphPath);

    console.log("Control Flow Steps:\n" + steps.join("\n"));
    console.log("\nGraph Descriptions:\n" + descriptions.join("\n"));

    fs.writeFileSync('control_flow_steps.txt', steps.join("\n"), 'utf-8');
    fs.writeFileSync('graph_descriptions.txt', descriptions.join("\n"), 'utf-8');
    console.log(" Steps saved to control_flow_steps.txt");
    console.log(" Descriptions saved to graph_descriptions.txt");
}

module.exports = graphToStepsWithDescription;
