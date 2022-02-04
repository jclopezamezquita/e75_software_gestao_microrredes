import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';
import { Measurements_24hours } from 'src/app/shared/model/measurements_24hours.model';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-pv-widget-area',
  templateUrl: './pv-area.component.html',
  styleUrls: ['./pv-area.component.scss']
})
export class PvAreaComponent {

  private intervalUpdate: any = null;

  public measurements_pv = new Array();
  
  public now1 = new Date();
  public now2 = new Date();
  public SP_Timezone = 3

  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

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
        text: 'Generation [kW]'
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

  constructor(private http: HttpClient) {

    this.http.get<Measurements_24hours>('http://localhost:8051/v1/api/node_measurement/last_24h/')
    .subscribe(
      data2 => {
        this.measurements_pv = [];
        this.measurements_pv.push(Math.abs(Number(data2.pv_t00)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t01)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t02)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t03)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t04)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t05)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t06)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t07)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t08)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t09)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t10)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t11)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t12)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t13)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t14)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t15)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t16)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t17)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t18)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t19)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t20)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t21)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t22)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t23)));
    
        this.chartOptions.series = [
          {
            type: 'line',
            name: 'pv',
            data: this.measurements_pv
          }
        ]
    
        this.updateFlag = true;
        if(this.measurements_pv.length) {
          this.updateData = true;
        }
    });

  }

  ngOnInit(): void { 

    this.chartOptions.title =  {
      text: this.label
    };

    this.intervalUpdate = setInterval(function(){
      // if(this.share.mode == MODES.PLAY) {
        this.showData();
      // }
    }.bind(this), 5000);

  }

  private showData(): void {
    this.http.get<Measurements_24hours>('http://localhost:8051/v1/api/node_measurement/last_24h/')
    .subscribe(
      data2 => {
        this.measurements_pv = [];
        this.measurements_pv.push(Math.abs(Number(data2.pv_t00)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t01)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t02)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t03)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t04)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t05)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t06)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t07)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t08)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t09)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t10)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t11)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t12)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t13)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t14)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t15)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t16)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t17)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t18)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t19)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t20)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t21)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t22)));
        this.measurements_pv.push(Math.abs(Number(data2.pv_t23)));
    
        this.chartOptions.series = [
          {
            type: 'area',
            name: 'pv',
            data: this.measurements_pv
          }
        ]
        
        this.now2 = new Date()
        this.chartOptions.plotOptions.series.pointStart = this.now2.setHours(this.now2.getHours()-this.SP_Timezone-23)   

        this.updateFlag = true;
        if(this.measurements_pv.length) {
          this.updateData = true;
        }
    });
  }

}
