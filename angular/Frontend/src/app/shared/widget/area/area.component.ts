import { Component, OnChanges, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';

@Component({
  selector: 'app-widget-area',
  templateUrl: './area.component.html',
  styleUrls: ['./area.component.scss']
})
export class AreaComponent {

  public now1 = new Date();
  public now2 = new Date();
  public SP_Timezone = 3

  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() meas_pcc = [];
  @Input() meas_pv = [];
  @Input() meas_genset = [];
  @Input() meas_bess = [];
  @Input() label: string;

  chartOptions: Highcharts.Options = {
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
    plotOptions: {
      series : {
        pointStart: this.now1.setHours(this.now1.getHours()-this.SP_Timezone-23),
        // pointStart: Date.UTC(2020, 2, 3),
        pointInterval: 3600 * 1000 // one hour
      }
    }

  }

  constructor() {  }

  ngOnInit(): void { }

  ngOnChanges(changes: SimpleChanges) {

    this.chartOptions.title =  {
      text: this.label
    };

    this.chartOptions.series = [
      {
        type: 'area',
        name: 'PCC',
        data: this.meas_pcc
      },{
        type: 'area',
        name: 'PV',
        data: this.meas_pv
      },{
        type: 'area',
        name: 'BESS',
        data: this.meas_bess
      },{
        type: 'area',
        name: 'GENSET',
        data: this.meas_genset
      }
    ]
    
    this.now2 = new Date()
    this.chartOptions.plotOptions.series.pointStart = this.now2.setHours(this.now2.getHours()-this.SP_Timezone-23)   

    this.updateFlag = true;
    if(this.meas_pcc.length) {
      this.updateData = true;
    }

  }

}