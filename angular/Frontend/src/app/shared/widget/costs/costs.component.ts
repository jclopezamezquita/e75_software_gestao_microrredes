import { Component, OnChanges, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';

@Component({
  selector: 'app-widget-costs',
  templateUrl: './costs.component.html',
  styleUrls: ['./costs.component.scss']
})

export class CostsComponent {

  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() data = [];

  chartOptions: Highcharts.Options = {
    title:  {
      text: 'old'
    }, 
    series: [
      {
        type: 'line',
        data: this.data
      }
    ]
  }
  
  constructor() {  }

  ngOnInit(): void { }

  ngOnChanges(changes: SimpleChanges) {
  
    this.chartOptions.title =  {
      text: 'Hourly Energy Prices ($/kWh)'
    };

    this.chartOptions.series[0] = {
      type: 'line',
      data: this.data
    }

    this.updateFlag = true;
    if(this.data.length) {
      this.updateData = true;
    }
    console.log("********* ngOnChanges ********")
    console.log(this.chartOptions.series[0].data)

  }

}
