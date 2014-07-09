 	// (C) February 2013 - Daniele Zanotelli

// This program is free software: you can redistribute it and/or modify
//     it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 2 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU General Public License for more details.

//     You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.


// Compose DataTables with D3.js

datatablesPlusD3 = {
    init : function ()
    {
	self = this;
	self.table_data = { "headers": ['id', 'surname', 'name', 'age',
					'fill'],
			    "data" : [ { 'id' : 1,
					 'surname' : 'Goof',
					 'name' : 'Goofy',
					 'age' : 25,
					 'fill' : 'red'
				       },
				       { 'id' : 11,
					 'surname' : 'Mouse',
					 'name' : 'Mickey',
					 'age' : 14,
					 'fill' : 'orange'
				       },
				       { 'id' : 30,
					 'surname' : 'Duck',
					 'name' : 'Donald',
					 'age' : 20,
					 'fill' : 'green'
				       } ]
			  };
	self.chart = undefined;
	self.main = undefined;
	self.margin = { top : 20, left : 60, bottom: 60, right: 20 };
	self.chart_w = 700;
	self.chart_h = 300;
	self.main_w = self.chart_w - self.margin.left - self.margin.right;
	self.main_h = self.chart_h - self.margin.top - self.margin.bottom;
	self.x = d3.scale.ordinal().rangeRoundBands([0, self.main_w], .1);
	self.y = d3.scale.linear().range([self.main_h, 0]);
    },
    go : function ()
    {
	this.init();
	this.init_chart();
	this.init_table();
	this.activate_datatable();
    },
    
    init_table : function ()
    {
	self = this;
	table = d3.select('body')
	    .append('div')
	    .attr('id', 'datatable-div')
	    .style('width', '40%')
	    .style('margin', '0 auto')
	    .append('table')
	    .attr('id', 'datatable-table')
	;
	
	cols = self.table_data.headers;
	
	var headers = table.append('thead').append('tr');
	h = headers.selectAll('th').data(cols);
	h.enter()
	    .append('th')
	    .text(function (d) { 
		return '' + d.charAt(0).toUpperCase() + d.substr(1);
	    })
	;
	
	table.append('tbody');
	
	var rows = table.select('tbody').selectAll('tr')
	    .data(self.table_data.data, function (d) { return d.id } )
	;
	rows.enter().append('tr').attr('class', 'data-entry');
	
	var cells = rows.selectAll('td').data( function (row) {
	    return cols.map(function (col_name) {
		return { k : col_name, v : row[col_name] };
	    })
	})
	;
	cells.enter()
	    .append('td')
	    .attr('class', function (d) { return d.k; })
	    .text(function (d) { return d.v; })
	;
    },
    
    activate_datatable : function ()
    {
	self = this;
	self.myTable = jQuery('#datatable-table').dataTable( {
	    "bSortClasses" : false,
	    "bPaginate" : false,
	    "bAutowidth" : true,
	    "sDom" : 'rftp',
	    "aoColumnDefs" : [ { "sWidth" : "200px", "aTargets" : [ "_all" ] } ],
	    "fnDrawCallback" : function () {
		self.update();
	    }
	});	
    },

    init_chart : function ()
    {
	self = this;
	self.chart = d3.select('body')
	    .append('div').attr('id', 'chart_cont')
	    .style('width', '50%')
	    .style('margin', '0 auto')
	    .style('margin-bottom', '50px')
	    .append('svg').attr('id', 'chart')
	    .attr('width', self.chart_w)
	    .attr('height', self.chart_h)
	;

	// add a rect frame
	self.chart.append('rect')
    	    .attr('width', self.chart_w)
	    .attr('height', self.chart_h)
    	    .attr('fill', '#eee')
	    .attr('stroke', '#222')
	    .attr('stroke-width', 1)
	;
	
	self.main = self.chart
	    .append('g')
	    .attr('transform',
		  'translate(' + self.margin.left + ',' + self.margin.top + ')')
	;
    
	xAxis = d3.svg.axis().scale(self.x).orient('bottom');
	yAxis = d3.svg.axis().scale(self.y).orient('left');
	
	self.x.domain([]);
	self.y.domain([]);
    
	self.main.append('g')
	    .attr('class', 'axis')
	    .attr('id', 'x-axis')
	    .attr('transform', 'translate(0, ' + (self.main_h) + ')')
	    .call(xAxis)
	;
	self.main.append('g')
	    .attr('id', 'y-axis')
	    .attr('class', 'axis')
	    .call(yAxis)
	;
    },
    
    update_dataset : function ()
    {
	self = this;
	myData = new Array();
	tr = document
	    .getElementById('datatable-table')
	    .getElementsByClassName('data-entry')
	;
	for (i=0; i<tr.length; i++) {
	    myData[i] = new Object();
	    for (hi in self.table_data.headers) {
		h = self.table_data.headers[hi];
		v = tr[i].getElementsByClassName(h)[0].innerHTML;
		if (isNaN(v))
		    myData[i][h] = v;
		else
		    myData[i][h] = +v;
	    }
	}
	return myData;
    },
    
    update_chart : function (newData)
    {
	self = this;
	// update x axis
	xAxis = d3.select('#x-axis').remove();
	self.x.domain(newData.map(function (d) { return d.surname; }));
	
	tick_pos = d3.range(newData.length);
	tick_labels = tick_pos.map(function (v) { return "item " + v; });
	
	xAxis = d3.svg.axis()
	    .scale(self.x)
	    .orient('bottom')
	    .ticks(newData.length)
	;
	
	self.main.append('g')	
    	    .attr('class', 'axis')
    	    .attr('id', 'x-axis')
    	    .attr('transform', 'translate(0, ' + (self.main_h) + ')')
    	    .call(xAxis)
	;
	
	// update y axis
	yAxis = d3.select('#y-axis').remove();
	self.y
	    .domain([0, d3.max(newData.map(function (o) { return o.age;}))])
	;
	yAxis = d3.svg.axis().scale(self.y).orient('left').ticks(5);
	self.main.append('g')
	    .attr('id', 'y-axis')
	    .attr('class', 'axis')
	    .call(yAxis)
	    .append("text")
	    .attr("transform", "rotate(-90)")
	    .attr("y", -50)
	    .attr("dy", ".71em")
	    .style("text-anchor", "end")
	    .text("Age");
	;
	
	
	// populate chart with data
	bars = self.main
	    .selectAll('rect')
	    .data(newData, function (k) { return k.id })
	;
	
	bars.enter()
	    .append('rect')
	    .attr('x', function (d) { return self.x(d.surname); })
	    .attr('width', self.x.rangeBand())
	    .attr('y', function (d) { return self.y(d.age); })
	    .attr('height', function (d)
		  { 
		      return self.main_h - self.y(d.age) -2;
		  }
		 )
	    .attr('fill', function (d) { return d.fill;})
	    .attr('stroke', 'grey')
	    .attr('stroke-width', 1)
	    .attr('opacity', 1)
	;
    
	bars.transition()
	    .delay(1200)
    	    .attr('x', function (d) { return self.x(d.surname); })
    	    .attr('width', self.x.rangeBand())
    	    .attr('height', function (d) 
		  { 
		      return self.main_h - self.y(d.age) -2;
		  }
		 )
    	    .attr('y', function (d) { return self.y(d.age); })
    	    .attr('fill', function (d) { return d.fill;})
    	    .attr('stroke', 'grey')
    	    .attr('stroke-width', 1)
	    .attr('opacity', 1)
	;
    
	bars.exit()
	    .transition()
	    .duration(1300)
	    .attr('opacity', 0.1)
	    .transition()
	    .delay(500)
	    .attr('height', 0)
	//	.attr('transform', 'translate(0,' + self.chart_h + ')')
	    .attr('y', function (d) { return self.chart_h *2 })
	//	.attr('width', 0)
	    .remove()
	;
    },
    update : function () {
	self = this;
	data = self.update_dataset();
	self.update_chart(data);
    },
};

