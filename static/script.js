function change()
{	
	document.getElementById("aggregate").setAttribute("style","display:inline;");
	document.getElementById("agg").setAttribute("placeholder","Percentage");
}
function change2()
{
		document.getElementById("aggregate").setAttribute("style","display:inline;");
		document.getElementById("agg").setAttribute("placeholder","CGPA");
}
function change3()
{	
	document.getElementById("aggregate2").setAttribute("style","display:inline;");
	document.getElementById("agg2").setAttribute("placeholder","Percentage");
}
function change4()
{
		document.getElementById("aggregate2").setAttribute("style","display:inline;");
		document.getElementById("agg2").setAttribute("placeholder","CGPA");
}
function gpa()
{
	document.getElementById("sgpa-disp").setAttribute("style","display:inline;");
	x=parseInt(document.getElementById("opr2").value);
	for( var i=1;i<x;i++)
	{
		z=i.toString()+" sem SGPA";
		y=document.createElement("INPUT");
		y.setAttribute("type","text");
		y.setAttribute("placeholder",z);
		y.setAttribute("style","border:1px solid black;");
		document.getElementById("sgpa").appendChild(y);
	}
}
