import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';


@Component({
  selector: 'app-widget-bars',
  templateUrl: './bars.component.html',
  styleUrls: ['./bars.component.scss']
})

export class BarsComponent {

  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() label: string;
  @Input() data = [];

  chartOptions: Highcharts.Options = {
    title:  {
      text: 'column'
    },
    yAxis: {
      title: {
        text: 'Active Power [kW]'
      }
    }, 
    legend: {
      enabled: false
    },
    credits: {
      enabled: false
    },
    series: [
      {
        type: 'bar',
        data: this.data
      }
    ]
    }
  
  
  constructor() {  }

  ngOnInit(): void { }

  ngOnChanges(changes: SimpleChanges) {
  
    this.chartOptions.title =  {
      text: this.label
    };

    this.chartOptions.series[0] = {
      type: 'column',
      data: this.data
    };

    this.updateFlag = true;
    if(this.data.length) {
      this.updateData = true;
    };
    console.log("********* ngOnChanges ********")
    console.log(this.chartOptions.series[0].data)

  }
}