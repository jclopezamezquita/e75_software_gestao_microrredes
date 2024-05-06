import { Component, OnChanges, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';

@Component({
  selector: 'app-widget-pie',
  templateUrl: './pie.component.html',
  styleUrls: ['./pie.component.scss']
})
export class PieComponent {
  
  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() meas_pcc_23: number;
  @Input() meas_pv_23: number;
  @Input() meas_genset_23: number;
  @Input() meas_bess_23: number;
  @Input() label: string;

  chartOptions: Highcharts.Options = {
    chart: {
      plotBackgroundColor: null,
	    plotBorderWidth: null,
	    plotShadow: false,
	    type: 'pie',
      borderWidth: 0,
      margin: [2, 2, 2, 2]
    },
    title:  {
      text: 'column'
    },
    credits: {
      enabled: false
    },
    yAxis: {
      title: {
        text: 'Values [kW]'
      }
    },
    xAxis: {
      type: 'datetime'
    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
      point: {
        valueSuffix: '%'
      }
    },
    exporting: {
      enabled: true
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
            format: '<b>{point.name}</b>: {point.percentage:.1f} %'
        }
      }
    },
    colors:['#4B4B4D', '#9DC8F0', '#F9B985', '#9AEE88'] // Negro para PV, Azul para PCC, Naranja para GENSET, verde para BESS
  }
  
  constructor() {  }

  ngOnInit(): void { }

  ngOnChanges(changes: SimpleChanges) {

    this.chartOptions.title =  {
      // text: this.label
      text: null
    };

    this.chartOptions.series = [
      {
        type: 'pie',
        name: 'Sources',
        colorByPoint: true,
        data: [{
            name: 'PV',
            y: Math.abs(this.meas_pv_23)
        }, {
            name: 'PCC',
            y: Math.max(0,this.meas_pcc_23)
        }, {
            name: 'GENSET',
            y: Math.abs(this.meas_genset_23)
        }, {
            name: 'BESS',
            y: Math.abs(Math.min(0,this.meas_bess_23))
        }]
      }
    ]
      
    this.updateFlag = true;
    this.updateData = true;
  }
}
