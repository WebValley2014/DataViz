/**
 * (C) July 2014 - FBK _ Fondazione Bruno Kessler - Web Valley 2014
 *  authors: Davide Farina - pilotapazzo@gmail.com
 *           Daniele Zanotelli - zanotelli@fbk.eu
 * 
 * This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */

var UTILS = {
    setCSSClass : function(element, CSSclass) {
        var classes = [];
        var classesStr = element.getAttribute('class');
        if (classesStr)
            classes = classesStr.split(' ');
        
        // check if CSSclass is already there
        for (var i in classes) {
            if (classes[i] == CSSclass)
                return true;
        }
        // else set it
        classes.push(CSSclass);
        // set the new class
        element.setAttribute('class', classes.join(' '));
        return true
    },
    delCSSClass : function (element, CSSclass) {
        var classes = element.getAttribute('class').split(' ');
        // check if CSSclass is already missing
        var found = false;
        for (var i in classes) {
            if (classes[i] == CSSclass) {
                found = true;
                break;
            }
        }
        if (found == false)
            return true;
        else { //let's remove it
            var classIdx;
            while ((classIdx = classes.indexOf()) > -1) {
                classes.splice(classIdx, 1);
            }
            // set class with the new value
            element.setAttribute('class', classes);
        }
    }
};

var CHART = {
    cont : undefined,
    go : function (r) {
        this._init(r);
        this._initChart();
        this.updateChart(2);
    },
    _init : function (r) {
        this.cont_id = 'chart',
        //this.width = 820,
        this.width = 1000,
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
	this.headers = []
        this.xValues = d3.range(10);
	this.colors = ["red", "green", "blue"];

	this._elaborateFile();
        // store file headers (OTU ids) into this.headers
	this._extractHeaders();
        
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
	//console.log(this.data);
	return true;
    },
    _elaborateFile : function () {
	//console.log(this.headers);
	this.lines = this.readFile.split("\n");
	for (var i = 0; i < this.lines.length; i++) {
	    this.file[i] = this.lines[i].split("\t");
	}
	for (var i = 0; i < 10; i++) {
	    for (var j = 0; j < 3; j++) {
		if (j == 0) 
		    this.data[i * 3] = this._getSum(i, "1");
		if (j == 1)
		    this.data[i * 3 + j] = 0;
		if (j == 2)
		    this.data[i * 3 + j] = this._getSum(i, "0");
	    }
	}
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
    },
    _extractHeaders: function() {
	var headers = [];
	for(i in this.file[1]) {
	    headers.push(this.file[1][i].split(";").slice(-2).join(";"));
	}
	this.headers = headers.slice(1, -1);
    },
    _createAxis : function () {
        self = this;
        //console.log(self.headers);

        // build x axis
        xAxis = d3.svg.axis().scale(this.x).orient('bottom');
        this.graph.append('g')
            .attr('id', 'xaxis')
            .attr('class', 'axis')
            .attr('transform', 'translate(0, ' + this.inner_h + ')')
            .call(xAxis)
	    .append("text")
	    .text("OTU id")
	    .attr("transform", "translate(" + this.inner_w + ", 50)")
	    .style("text-anchor", "end")
        ;

        //xAxis.tickValues(self.headers);
        //self.xAxis = xAxis;

        // build y axis
        yAxis = d3.svg.axis().scale(this.y).orient('left');
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
        //this.x.domain(this.headers);
        this.x.domain(this.xValues);
        this._createAxis();
    },
    drawChart : function () {
	var self = this;
	var labels = this.headers;
	var getColor = this.getColor;
	//console.log(this.colors);
        bars = this.graph.selectAll('rect.mybar').data(this.data);
        //        console.log(this.data);
        
        bars.enter().append('rect')
	    //.attr('class', 'mybar')
            .attr('class', function (d, i) {
                return 'mybar ' + 'bar' + parseInt(i/3);
            })
	    .attr('width', self.x.rangeBand() / 4)
	    .attr('x', function (d, i) {
                //DEBUG
                //console.log(i + " " + d);
                //console.log('offset ' + self.getOffset(i));
                
                return self.x(self.xValues[self.getLabelIndex(i)]) + 
                //return self.x(self.headers[self.getLabelIndex(i)]) + 
                    self.getOffset(i) + 
                    self.x.rangeBand() / 2 - 5; 
            })
	    .attr('y', self.y(0))
	    .attr('fill', function (d, i) { return self.getColor(i);})
	    .attr('stroke', 'grey')
	    .attr('stroke-width', 1)
	    .attr('opacity', 1)
        ;

        bars.transition()	    
            .attr('y', function (d) { return self.y(d); })
	    .attr('height', function (d) {
	    	return self.inner_h - self.y(d);
	    }
	    	 )
        ;
        
        bars.exit()
            .transition()
            .attr('y', self.y(0))
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
};

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
	for(var i in this.headers) {
	    //console.log(i);
	    //console.log(this.headers[i]);
	    var h = document.createElement("th");
	    h.innerHTML = this.headers[i]
            if (parseInt(i) > 0 && parseInt(i) < 11)
                h.innerHTML += " (OTU #" + i + ")";
	    row.appendChild(h);
	}
	thead.appendChild(row);
	table.appendChild(thead);
	//body
	var tbody = document.createElement("tbody");
	for (var i = 2; i < this.file.length; i++) {
	    var line = this.file[i];
	    var newI = i;
	    var row = document.createElement("tr");
	    row.setAttribute('value', i);

            UTILS.setCSSClass(row, (i+1) % 2 ? 'odd' : 'even');
            
	    row.onclick = function() {
                // delete all the enlighted class from table
	    	d3.selectAll("tbody tr").classed("enlighted", false);
                // set the enlighted class just on active row
                UTILS.setCSSClass(this, 'enlighted');
	    	//this.setAttribute("class", "enlighted");
	    	//console.log(newI);
	    	return CHART.updateChart(this.getAttribute('value'));
	    };
	    
	    for(var j in line) {
		var td = document.createElement("td");
		td.innerHTML = line[j];
		if(j == 0) {
                    UTILS.setCSSClass(td, 'label');
		    //td.setAttribute("class", "label");
                }
		else if (j > 0 && j < line.length -1) {
                    UTILS.setCSSClass(td, 'value');
		    //td.setAttribute("class", "value");
                }
		else {
                    UTILS.setCSSClass(td, 'flag');
		    //td.setAttribute("class", "flag");
                }
		row.appendChild(td);
	    }
	    tbody.appendChild(row);
	}
	table.appendChild(tbody);
	document.getElementById(this.cont_id).appendChild(table);
    }
}

