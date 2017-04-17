function experiment_chart(labels, data, index) {
    // Get context with jQuery - using jQuery's .get() method.
    var ctx = $("#inputTextResultsChart").get(0).getContext("2d");
    var canvas=document.getElementById('WordStat');
    var wordctx=canvas.getContext('2d');
     $("#help")
    .mouseover(function(){
        $("#helptxt").text("Click and drag to zoom graph");
        })
    .mouseout(function(){
        $("#helptxt").text("");

    });	
    //Create an array of colors
   //var colors = ["rgba(180,180,180,1)", "rgba(180,180,50,0.8)", "rgba(180,50,180,0.8)", "rgba(50,180,180,0.8)", "rgba(180,50,50,1)", "rgba(50,180,50,0.8)", "rgba(50,50,180,0.8)", "rgba(50,100,180,0.8)"];
    var colors=["#2A0A0A","#ecc10f","#37d008","#070ab2","#8507b2", "#c11196", "#ee5190"];
     // for OOV words
    var max = 0;
        for(var key in data) {
            for(i of data[key]) {
                if(i != "***OOV***" && i > max) {
                    max = i;
                }
            }
        }
    max = Math.ceil(max + 0.01);	
    datasets = []
    var count = -1;
    for(var key in data) {

        if (count < 7)
            count += 1;
        pts = $.map(data[key], function(val, i) {
            if(val == "***OOV***") return max;
             else return val;
        });

        dataset = { label: key,
            fillColor: colors[count],
            strokeColor: colors[count],
            pointColor: colors[count],
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: colors[count],
            data: pts
        };

        datasets.push(dataset)
    }

    // This will get the first returned node in the jQuery collection.
    var data = {
        labels: labels,
        datasets: datasets
    };

    var options = {

        ///Boolean - Whether grid lines are shown across the artchart
        scaleShowGridLines : true,

        //String - Colour of the grid lines
        scaleGridLineColor : "rgba(0,0,0,.10)",

        //Boolean - Whether the line is curved between points
        bezierCurve : false,

        //Number - Tension of the bezier curve between points
        bezierCurveTension : 0.0,

        //Boolean - Whether to show a dot for each point
        pointDot : true,

        //Number - Radius of each point dot in pixels
        pointDotRadius : 4,

        //Number - Pixel width of point dot stroke
        pointDotStrokeWidth : 1,

        //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
        pointHitDetectionRadius : 20,

        //Boolean - Whether to show a stroke for datasets
        datasetStroke : true,

        //Number - Pixel width of dataset stroke
        datasetStrokeWidth : 2,

        //Boolean - Whether to fill the dataset with a colour
        datasetFill : false,

        //String - A legend template
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"> &nbsp;&nbsp;</span> <%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",
        
        showScale: true,
        
        scaleLabel: "<%if(value!=" + max + "){%> <%=value%> <%} else {%> OOV <%}%>",
        
        animation:false,

        tooltipYPadding: 6,

        tooltipXPadding: 6,

        //tooltipTemplate: "<%if (label){%><%=label%>: <%}%>",
        tooltipTemplate: "<%if (label){%><%=label%>: <%}%>: <%if(value!=" + max + "){%> <%=value%><%} else {%>***OOV***<%}%>",

        multiTooltipTemplate: "<%=datasets[i]%>: <%if(value!=" + max + "){%> <%=value%><%} else {%>***OOV***<%}%>"

    };

    htmlforGraph="<canvas id='inputTextResultsChart' width='900' height='400'>"
    holder=document.getElementById('inputTextResultsChart');
    holder.innerHTML=htmlforGraph;

    //var resultsChart = new Chart(ctx).Line(data, options);

    //*************My changes *********************************************

    var worddict=[];
    var tmpword;

    //Returns labels == individual words
    //Returns count of each word
    function wordcount(word,arr)
    {
       var count = 0;
       var temp=arr.dataPoints;
       for(var i=0; i< temp.length;i++)
       {
            if(word.toLowerCase() == temp[i].label.toLowerCase())
            {
                count=count +1;
            }
       }
       return count;
    }

    function maxw(word, val, arr)
    {
       var max1=val;
       //console.log(val + word);
       var temp=arr.dataPoints;
       if(wordcount(word.toLowerCase(), arr) == 1)
        {
         if(max1 == max)
            return "No Stat Found";

        }
       if(max1 == max)
       {
            max1 = 0;
       }
       for(var i=0; i< temp.length;i++)
       {
           if(word.toLowerCase() == temp[i].label.toLowerCase())
           {
                if(max1>temp[i].y && temp[i].y != max)
                {
                    max1=temp[i].y;
                }
           }
       }
       return max1;
    }

    function minw(word, val, arr)
    {
        var min=val;

        if(wordcount(word.toLowerCase(), arr) == 1)
        {
         if(min == max)
            return "No Stat Found";

        }
        if(min == max)
          min=0;
       for(var i=0; i< temp.length;i++)
       {

           if(word.toLowerCase() == temp[i].label.toLowerCase())
           {
                if(min<temp[i].y && temp[i].y != max )
                {
                    min=temp[i].y;
                }
           }
       }
       return min;

    }

    function standdev(word, arr)
    {
       var sdarr=[];
       var sum=0;
       var mean;
       var varience=0;
       var temp=arr.dataPoints;
       for(var i=0;i<temp.length;i++)
        {
            if(word.toLowerCase() == temp[i].label.toLowerCase() && temp[i].y != 5)
            {
                sdarr.push(temp[i].y);
                sum+=temp[i].y
            }
        }

        mean=sum/sdarr.length;

        for(var j=0; j<sdarr.length; j++)
        {
            varience=varience+Math.pow((mean-sdarr[j]),2);
        }

        return Math.sqrt(varience);

    }

    function isapplicable(word, val, arr)
    {
        var tmp=val;

        if(wordcount(word.toLowerCase(), arr) == 1)
        {
         if(tmp == max)
            return true;

        }
        else
        return false;

    }

    //Multiple line graphs
    var maxWords=30;
    var startindex = 0;
    var endindex;
    //Max number of items that can be displayed
    n = data.labels.length;
    endindex = n - 1;
    if(n > maxWords)
    {
        if (index < maxWords / 2)
            endindex = maxWords - 1;
        else if (index >= n - maxWords / 2)
            startindex = n - maxWords;
        else
        {
            startindex = index - maxWords / 2;
            endindex = index + maxWords / 2 - 1;
        }
    }
    //set page numbers
    var dat=[];
    var datpnt=[];
    var dar=data.datasets;
    var temp=[];
    cnt=-1;
    for(i=0;i<data.datasets.length; i++)
    {
     cnt++;
         // Find the maximum value in the data, and round it up a bit

         datpnt=[];
        for(j=startindex;j<=endindex;j++)
        {
            var val=data.datasets[i].data[j];
            var lb= data.labels[j];
            var datpoint={label: data.labels[j], y: val};
            datpnt.push(datpoint);
        }



        dat1={
            type: "line",
            dataPoints: datpnt,
            showInLegend: true,
            color: colors[cnt],
            click: function(e)
            {
                canvas.height = 200;
                wordctx.clearRect(0,0, canvas.width, canvas.height);
                wordctx.fillStyle="#333";
                wordctx.font="20px arial ";
                var ctx=isapplicable(e.dataPoint.label,e.dataPoint.y,e.dataSeries);
                if(ctx)
                {
                wordctx.fillText("Statistics for word : '' "+ e.dataPoint.label +" '' No data to display", 30, 50);
               // wordctx.font="16px arial ";
               // wordctx.fillText("No data to display", 50, 80);//30, 100
                }
                else
                {
                wordctx.fillText("Statistics for word : '' "+ e.dataPoint.label +" ''", 30, 50);
                wordctx.font="16px arial ";
                wordctx.fillText("Frequency : " + wordcount(e.dataPoint.label,e.dataSeries), 50, 80);//30, 100
                wordctx.fillText("Maximum Surprisal : " + maxw(e.dataPoint.label, e.dataPoint.y, e.dataSeries), 50, 110);//30, 140
                wordctx.fillText("Minimum Surprisal : " + minw(e.dataPoint.label, e.dataPoint.y, e.dataSeries), 50, 140);//30, 180
                wordctx.fillText("Standard Deviation : " + standdev(e.dataPoint.label, e.dataSeries), 50, 170);//30, 220
                }
            },
            name:data.datasets[i].label
        };

        dat.push(dat1);

    }
    var datapoint=[];
    //for(i=0; i< data.labels.length; i++)
    for(i = startindex; i < endindex; i++)
    {
        datapoints={label: data.labels[i], y: pts[i]};
        datapoint.push(datapoints);
    }

    var chart=new CanvasJS.Chart("CanvasTest",{
        theme: "theme2",
        zoomEnabled: true,
        animationEnabled: true,
	backgroundColor: "#fbfff9",
        exportFileName: "Surprisal Graph",
        exportEnabled: true,
        axisX:{labelFontSize: 10, labelFontStyle: "oblique", titleFontFamily: "arial", interval: 1, labelAngle: 30, labelFontColor:"#2A0A0A"  },
        axisY:{includeZero: false, labelFontColor:"#2A0A0A",gridColor:"#d9dfe3" },
        data:dat,
        toolTip:{content: function(e){
                var content=e.entries[0].dataPoint.y == max? "***OOV***" : e.entries[0].dataPoint.label+": " +e.entries[0].dataPoint.y;
                return content;
            }
        }
    });
    chart.render();

}

function searchWord(context_start, context_end, searchWord)
{
    var concTable   = document.getElementById("concordance");

    concTable.rows[0].cells[0].innerHTML = "<b>Search Word: <i>"+ searchWord +"</i></b>";

    var rangeOfWords = context_start.length;
    for (var i = 0; i < rangeOfWords; i++)
    {
        concTable.rows[i].cells[0].innerHTML = context_start[i] + "<u><b>" + searchWord + "</u></b>" + context_end[i];
    }
    var isFound = 1;
    /*var rangeOfWords = 10;
    var n = labels.length - 1;
    if (n <= 2)
        rangeOfWords = n + 1;
    else if (n < rangeOfWords)
    {
        rangeOfWords = n / 2;
    }
    var isFound = 0;
    var rowNum = 0;
    for (var i = 0; i <= n; i++)
    {
        var startIndex = 0;
        var endIndex = n;
        var sentencePart1 = "";
        var sentencePart2 = "";
        var sentencePart3 = "";
        if (labels[i] == searchWord)
        {
            isFound = 1;
            if (i == 0)
                endIndex = 2 * rangeOfWords;
            else if (i < rangeOfWords)
                endIndex = 2 * rangeOfWords - i + 1;
            else if (i >= n - rangeOfWords)
                startIndex = n - 2 * rangeOfWords -1;
            else
            {
                startIndex = i - rangeOfWords;
                endIndex = i + rangeOfWords;
            }
            //console.log(startIndex, i, endIndex, rangeOfWords, n);

            if (startIndex != 0)
                sentencePart1 = "...";
            for (var j = startIndex; j < i; j++)
                sentencePart1 = sentencePart1.concat(labels[j], " ");
            sentencePart2 = labels[i];
            for (var j = i + 1; j <= endIndex; j++)
                sentencePart3 = sentencePart3.concat(" ", labels[j]);
            if (endIndex != n)
                sentencePart3 = sentencePart3.concat("...");
            try
            {
                concTable.rows[++rowNum].cells[0].innerHTML = sentencePart1 + "<u><b>" + sentencePart2 + "</u></b>" + sentencePart3;
            }
            catch(err){}
        }
    }*/
    var tableDiv = document.getElementById("concordanceBlock");
    var errorMsg = document.getElementById("notFoundMsg");
    document.getElementById("tableHeader").innerHTML = "Search word: " + searchWord;
    if (searchWord != "")
    {
        if (isFound)
        {
            tableDiv.style.display = 'block';
            errorMsg.style.display = 'none';
        }
        else
        {
            tableDiv.style.display = 'none';
            errorMsg.style.display = 'block';
        }
    }
    else
    {
        tableDiv.style.display = 'none';
        errorMsg.style.display = 'none';
    }
    var pages = Math.ceil(concTable.rows.length / 10);
    if (pages > 1)
    {
        for (var i = 1; i <= 10; i++)
            concTable.rows[i].style.display = 'block';
        document.getElementById("nextPageBtn").disabled = false;
        document.getElementById("prevPageBtn").disabled = true;
        document.getElementById("totalPage").innerHTML = pages;
        document.getElementById("currentPage").innerHTML = 1;
        document.getElementById("tablePage").innerHTML = "Showing page 1 of " + pages;
    }
}

function nextPage()
{
    console.log("NextPage");
    var concTable   = document.getElementById("concordance");
    currentPage = parseInt(document.getElementById("currentPage").innerHTML, 10);
    var hideOffset = 10 * (currentPage - 1);
    var showOffset = 10 * currentPage;
    console.log(hideOffset, showOffset);
    for (var i = 1; i <= 10; i++)
    {
        try {
        concTable.rows[hideOffset + i].style.display = 'none';
        }
        catch(err){}
    }
    for (var i = 1; i <= 10; i++)
    {
        try {
        concTable.rows[showOffset + i].style.display = 'block';
        }
        catch(err){}
    }
    pages = parseInt(document.getElementById("totalPage").innerHTML, 10);
    currentPage += 1;
    if (currentPage == pages)
        document.getElementById("nextPageBtn").disabled = true;
    else if (currentPage == 2)
        document.getElementById("prevPageBtn").disabled = false;
    document.getElementById("tablePage").innerHTML = "Showing page " + currentPage + " of " + pages;
    document.getElementById("currentPage").innerHTML = currentPage;
}

function previousPage()
{
    console.log("PrevPage");
    var concTable   = document.getElementById("concordance");
    currentPage = parseInt(document.getElementById("currentPage").innerHTML, 10);
    var hideOffset = 10 * (currentPage - 1);
    var showOffset = 10 * (currentPage - 2);
    console.log(hideOffset, showOffset);
    for (var i = 1; i <= 10; i++)
    {
        try {
        concTable.rows[hideOffset + i].style.display = 'none';
        }
        catch(err){}
    }
    for (var i = 1; i <= 10; i++)
    {
        try {
        concTable.rows[showOffset + i].style.display = 'block';
        }
        catch(err){}
    }
    pages = parseInt(document.getElementById("totalPage").innerHTML, 10);
    currentPage -= 1;
    if (currentPage == 1)
        document.getElementById("prevPageBtn").disabled = true;
    else if (currentPage < pages)
        document.getElementById("nextPageBtn").disabled = false;
    document.getElementById("tablePage").innerHTML = "Showing page " + currentPage + " of " + pages;
    document.getElementById("currentPage").innerHTML = currentPage;
}
