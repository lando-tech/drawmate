using DrawmateLib.DocumentContexts;
using DrawmateLib.Builders;

var drawmateContext = new DrawmateContext();
var mxCellBuilder = new MxCellBuilder();
var mxStyleBuilder = new MxStyleBuilder();

var mxCellOne = mxCellBuilder
    .Create(
        "Cell 1", 
        mxStyleBuilder
            .Create().Rectangle().Build(true).Value)
    .WithGeometry(400.0m, 400.0m, 50, 50)
    .Build();

drawmateContext.AddMxCell(mxCellOne);
drawmateContext.SaveDiagram("/home/aaron/Documents/drawmate.drawio.xml");