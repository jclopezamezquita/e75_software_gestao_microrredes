import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';
import { Measurements_24hours } from 'src/app/shared/model/measurements_24hours.model';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-soc-widget-area',
  templateUrl: './soc-area.component.html',
  styleUrls: ['./soc-area.component.scss']
})

export class SocAreaComponent {

  private intervalUpdate: any = null;

  public measurements_bess_soc = new Array();
  
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

  constructor(private http: HttpClient) {

    this.http.get<Measurements_24hours>('http://localhost:8051/v1/api/node_measurement/last_24h/')
    .subscribe(
      data2 => {
        this.measurements_bess_soc = [];
        this.measurements_bess_soc.push(Number(data2.bess_soc_t00));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t01));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t02));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t03));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t04));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t05));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t06));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t07));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t08));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t09));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t10));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t11));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t12));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t13));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t14));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t15));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t16));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t17));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t18));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t19));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t20));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t21));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t22));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t23));
        // console.log("this.measurements_bess_soc: ");
        // console.log(this.measurements_bess_soc);
    
        this.chartOptions.series = [
          {
            type: 'line',
            name: 'SOC',
            data: this.measurements_bess_soc
          }
        ]
    
        this.updateFlag = true;
        if(this.measurements_bess_soc.length) {
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
        this.measurements_bess_soc = [];
        this.measurements_bess_soc.push(Number(data2.bess_soc_t00));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t01));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t02));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t03));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t04));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t05));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t06));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t07));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t08));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t09));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t10));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t11));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t12));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t13));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t14));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t15));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t16));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t17));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t18));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t19));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t20));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t21));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t22));
        this.measurements_bess_soc.push(Number(data2.bess_soc_t23));
        // console.log("this.measurements_bess_soc: ");
        // console.log(this.measurements_bess_soc);
    
        this.chartOptions.series = [
          {
            type: 'area',
            name: 'SOC',
            data: this.measurements_bess_soc
          }
        ]
        
        this.now2 = new Date()
        this.chartOptions.plotOptions.series.pointStart = this.now2.setHours(this.now2.getHours()-this.SP_Timezone-23)   

        this.updateFlag = true;
        if(this.measurements_bess_soc.length) {
          this.updateData = true;
        }
    });
  }
}