var CHART = {
    cont : undefined,
    go : function (r) {
        this._init(r);
        this._initChart();
	this.updateAxis();
	this.drawChart();
    },
    _init : function (r) {
        this.cont_id = 'chart',
        this.width = 820,
        this.height = 500,
        this.margin = { top : 30, right : 30, bottom : 100, left : 100 },
        this.inner_w = this.width - this.margin.left - this.margin.right;
        this.inner_h = this.height - this.margin.top - this.margin.bottom;
	this.labels = [];
	this.readFile = r;
	this.OTUs = [];
	this.statuslist = [];
	this.file = [];
        this.data = [];
	this.offset = 20;
	this.headers = [];
	this.colors = ["red", "green", "blue"];

	this.ElaborateFile();
        
        this.x = d3.scale.ordinal().rangeRoundBands([0, this.inner_w]);
        this.y = d3.scale.linear().range([this.inner_h, 0]);


    },
    _updateData : function (rowN) {
	self = this;
	if(rowN < 2 || rowN > self.file.length)
	    return false;
        var line = self.file[rowN].slice(1, -1);
	//console.log(line);
	for(var i = 1, j = 0; i < 30; i+= 3, j++)
	    this.data[i] = line[j];
	console.log(this.data);
	return true;
    },
    ElaborateFile : function () {
	console.log(this.headers);
	this.lines = this.readFile.split("\n");
	for(var i = 0; i < this.lines.length; i++) {
	    var line = this.lines[i];
	   /* if(i == 0) {
		//console.log(headers);
		for(var j = 1; j < 11; j++) { 
		    var h = this.headers[j];
		    //console.log(h);
		    //this.labels.push("A" + h);
		    this.labels.push(h);
		    //this.labels.push("B" + h);
		}
	    }*/
	    // this.file.push([]);
	    this.file[i] = line.split("\t");
	}
	for(var i = 0; i < 10; i++) {
	    for(var j = 0; j < 3; j++) {
		if(j == 0) 
		    this.data[i * 3] = this._getSum(i, "1");
		if (j == 1)
		    this.data[i * 3 + j] = 0;
		if(j == 2)
		    this.data[i * 3 + j] = this._getSum(i, "0");
	    }
	}
	this._extractHeaders();
	//console.log(this.data.length);
	//console.log(this.labels.length);
    },
    _getSum: function(column, which) {
	var sum = 0;
	for(var i = 2; i < this.file.length; i++)
	    if(this.file[i][11] == which)
		sum += parseFloat(this.file[i][column + 1]);
	return sum;
    },
    _initChart : function() {
        this.svg = d3.select('#' + this.cont_id)
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height)
        ;
        // add a rect frame
        this.svg.append('rect')
            .attr('fill', '#eee')
            .attr('stroke', '#222')
            .attr('stroke-width', 1)
            .attr('height', this.height)
            .attr('width', this.width)
        ;
        this.graph = this.svg.append('g')
            .attr('transform',
                  'translate(' + this.margin.left + ',' + this.margin.top + ')')
        ;
	//set xAxis domain
	this.x.domain(this.headers);
	console.log(this.headers);
    },
    _extractHeaders: function() {
	var headers = [];
	for(i in this.file[1]) {
	    headers.push(this.file[1][i].split(";").slice(-2).join(";"));
	}
	this.headers = headers.slice(1, -1);
    },
    updateChart : function () {
        this._updateData();
        this._createAxis();
    },


    _createAxis : function () {        
        xAxis = d3.svg.axis().scale(this.x).orient('bottom');
        yAxis = d3.svg.axis().scale(this.y).orient('left');
        
        this.graph.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(0, ' + this.inner_h + ')')
            .call(xAxis)
	    .append("text")
	    .text("OTU id")
	    .attr("transform", "translate(" + this.inner_w + ", 50)")
	    .style("text-anchor", "end")

        ;

        this.graph.append('g')
            .attr('class', 'axis')
            .call(yAxis)
	    .append("text")
	    .text("Relative Abundance")
	    .attr("transform", "rotate(-90) translate(0, -50)")
	    .style("text-anchor", "end")
        ;
    },
    _removeAxis : function () {
        d3.selectAll('g.axis').remove();
    },
    updateAxis : function (N) {
	if (!N)
	    N = 100;
        this._removeAxis();
        //this.y.domain([0, d3.max(this.data)]);
	this.y.domain([0, N]);
	//this.y.domain([0, 110]);
        this._createAxis();
    },
    
    drawChart : function () {
	var self = this;
        var x = this.x;
        var y = this.y;
	var labels = this.headers;
	var getLabelIndex = this.getLabelIndex;
	var getColor = this.getColor;
	//console.log(this.colors);
        bars = this.graph.selectAll('rect.mybar').data(this.data);

        bars.enter().append('rect')
	    .attr('class', 'mybar')
	    .attr('width', self.x.rangeBand() / 4)
	    .attr('x', function (d, i) { return x(labels[getLabelIndex(i)]) + self.getOffset(i) + self.x.rangeBand() / 2 - 5; })
	    .attr('y', y(0))
	    .attr('fill', function (d, i) { return self.getColor(i);})
	    .attr('stroke', 'grey')
	    .attr('stroke-width', 1)
	    .attr('opacity', 1)
        ;

        bars.transition()	    
            .attr('y', function (d) { return y(d); })
	    .attr('height', function (d)
	    	  { 
	    	      return self.inner_h - y(d);
	    	  }
	    	 )
        ;
        
        bars.exit()
            .transition()
            .attr('y', y(0))
	    .attr('height', 0)
            .remove()
        ;

        
    },
    getOffset: function(dataIndex) {
	if((dataIndex % 3) == 0)
	    return -this.offset;
	if((dataIndex % 3) == 1)
	    return 0;
	if((dataIndex % 3) == 2)
	    return this.offset;
    },
    getLabelIndex: function(dataIndex) {
	return parseInt(Math.abs(dataIndex / 3));
    },
    getColor: function(dataIndex) {
	return this.colors[dataIndex % 3];
    },
    updateChart : function (rowN) {
	if(!(this._updateData(rowN)))
	    return false;
        this.updateAxis();
        this.drawChart();
    }
    
    
    

}

var TABLE = {
    go:function() {
	this._init();
	this._buildTable();
    },
    _init : function() {
	this.cont_id = "data-table";
	this.file = undefined;
	this.headers = undefined;

	this._loadData();
	this._extractHeaders();
    },
    
    _loadData : function() {
	this.file = CHART.file;
    },
    _extractHeaders: function() {
	var headers = [];
	for(i in this.file[1]) {
	    headers.push(this.file[1][i].split(";").slice(-2).join(";"));
	}
	this.headers = headers;
    },
    _buildTable: function() {
	var table = document.createElement("table");
	var thead = document.createElement("thead");
	var row = document.createElement("tr");
	for(i in this.headers) {
	    //console.log(i);
	    //console.log(this.headers[i]);
	    var h = document.createElement("th");
	    h.innerHTML = this.headers[i];
	    row.appendChild(h);
	}
	thead.appendChild(row);
	table.appendChild(thead);
	//body
	var tbody = document.createElement("tbody");
	for(var i = 2; i < this.file.length; i++) {
	    var line = this.file[i];
	    var newI = i;
	    var row = document.createElement("tr");
	    row.setAttribute('value', i);
	    row.onclick = function() { 
	    	d3.selectAll("tbody tr").classed("enlighted", false);
	    	this.setAttribute("class", "enlighted");
	    	//console.log(newI);
	    	return CHART.updateChart(this.getAttribute('value'));
	    };
	    
	    for(var j in line) {
		var td = document.createElement("td");
		td.innerHTML = line[j];
		if(j == 0)
		    td.setAttribute("class", "label");
		else if(j > 0 && j < line.length -1)
		    td.setAttribute("class", "value");
		else
		    td.setAttribute("class", "flag");
		row.appendChild(td);
	    }
	    tbody.appendChild(row);
	}
	table.appendChild(tbody);
	document.getElementById(this.cont_id).appendChild(table);
    }
}

