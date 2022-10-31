import { Component, OnChanges, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';

@Component({
  selector: 'app-pv-widget-area',
  templateUrl: './pv-area.component.html',
  styleUrls: ['./pv-area.component.scss']
})
export class PvAreaComponent {

  public now1 = new Date();
  public now2 = new Date();
  public SP_Timezone = 3
  public meas_pv_aux = new Array();

  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() meas_pv = [];
  @Input() label: string;

  chartOptions: Highcharts.Options = {
    title:  {
      text: 'column'
    },
    legend: {
      enabled: false
    },
    credits: {
      enabled: false
    },
    yAxis: {
      title: {
        text: 'Active Power [kW]'
      }
    },
    xAxis: {
      type: 'datetime'
    },
    plotOptions: {
      series : {
        pointStart: this.now1.setHours(this.now1.getHours()-this.SP_Timezone-23),
        // pointStart: Date.UTC(2020, 2, 3),
        pointInterval: 3600 * 1000 // one hour
      }
    },
    chart: {
      backgroundColor: null,
      borderWidth: 0,
      // margin: [2, 2, 2, 2],
      // height: 60
    },
    tooltip: {
        xDateFormat: 'Time: %Y-%m-%dT%H',
        shared: true
    }
  }

  constructor() {  }

  ngOnInit(): void { }

  ngOnChanges(changes: SimpleChanges) {

    this.chartOptions.title =  {
      text: this.label
    };

    for (let i = 0; i < this.meas_pv.length; i++) {
      this.meas_pv_aux.push(Math.abs(this.meas_pv[i]));
    }

    this.chartOptions.series = [
      {
        type: 'area',
        name: 'PV',
        data: this.meas_pv_aux
      }
    ]

    this.now2 = new Date()
    this.chartOptions.plotOptions.series.pointStart = this.now2.setHours(this.now2.getHours()-this.SP_Timezone-23)   

    this.updateFlag = true;
    if(this.meas_pv.length) {
      this.updateData = true;
    }
    
    this.meas_pv_aux = [];

  }
}
