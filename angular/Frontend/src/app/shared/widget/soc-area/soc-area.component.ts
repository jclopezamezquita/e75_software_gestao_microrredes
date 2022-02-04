import { Component, OnChanges, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';

@Component({
  selector: 'app-soc-widget-area',
  templateUrl: './soc-area.component.html',
  styleUrls: ['./soc-area.component.scss']
})

export class SocAreaComponent {

  public now1 = new Date();
  public now2 = new Date();
  public SP_Timezone = 3

  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() meas_bess_soc = [];
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
        text: 'SOC [pu]'
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
        name: 'SOC',
        data: this.meas_bess_soc
      }
    ]

    this.now2 = new Date()
    this.chartOptions.plotOptions.series.pointStart = this.now2.setHours(this.now2.getHours()-this.SP_Timezone-23)   

    this.updateFlag = true;
    if(this.meas_bess_soc.length) {
      this.updateData = true;
    }
  }
}