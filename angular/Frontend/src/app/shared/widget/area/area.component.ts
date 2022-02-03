import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';
import { Measurements_24hours } from 'src/app/shared/model/measurements_24hours.model';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-widget-area',
  templateUrl: './area.component.html',
  styleUrls: ['./area.component.scss']
})
export class AreaComponent {

  private intervalUpdate: any = null;

  public measurements_pcc = new Array();
  public measurements_pv = new Array();
  public measurements_genset = new Array();
  public measurements_bess = new Array();
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
    yAxis: {
      title: {
        text: 'Values [kW]'
      }
    },
    xAxis: {
      title: {
        text: 'Time'
      },
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
        this.measurements_pcc = [];
        this.measurements_pcc.push(Number(data2.pcc_t00));
        this.measurements_pcc.push(Number(data2.pcc_t01));
        this.measurements_pcc.push(Number(data2.pcc_t02));
        this.measurements_pcc.push(Number(data2.pcc_t03));
        this.measurements_pcc.push(Number(data2.pcc_t04));
        this.measurements_pcc.push(Number(data2.pcc_t05));
        this.measurements_pcc.push(Number(data2.pcc_t06));
        this.measurements_pcc.push(Number(data2.pcc_t07));
        this.measurements_pcc.push(Number(data2.pcc_t08));
        this.measurements_pcc.push(Number(data2.pcc_t09));
        this.measurements_pcc.push(Number(data2.pcc_t10));
        this.measurements_pcc.push(Number(data2.pcc_t11));
        this.measurements_pcc.push(Number(data2.pcc_t12));
        this.measurements_pcc.push(Number(data2.pcc_t13));
        this.measurements_pcc.push(Number(data2.pcc_t14));
        this.measurements_pcc.push(Number(data2.pcc_t15));
        this.measurements_pcc.push(Number(data2.pcc_t16));
        this.measurements_pcc.push(Number(data2.pcc_t17));
        this.measurements_pcc.push(Number(data2.pcc_t18));
        this.measurements_pcc.push(Number(data2.pcc_t19));
        this.measurements_pcc.push(Number(data2.pcc_t20));
        this.measurements_pcc.push(Number(data2.pcc_t21));
        this.measurements_pcc.push(Number(data2.pcc_t22));
        this.measurements_pcc.push(Number(data2.pcc_t23));    
        
        this.measurements_pv = [];
        this.measurements_pv.push(Number(data2.pv_t00));
        this.measurements_pv.push(Number(data2.pv_t01));
        this.measurements_pv.push(Number(data2.pv_t02));
        this.measurements_pv.push(Number(data2.pv_t03));
        this.measurements_pv.push(Number(data2.pv_t04));
        this.measurements_pv.push(Number(data2.pv_t05));
        this.measurements_pv.push(Number(data2.pv_t06));
        this.measurements_pv.push(Number(data2.pv_t07));
        this.measurements_pv.push(Number(data2.pv_t08));
        this.measurements_pv.push(Number(data2.pv_t09));
        this.measurements_pv.push(Number(data2.pv_t10));
        this.measurements_pv.push(Number(data2.pv_t11));
        this.measurements_pv.push(Number(data2.pv_t12));
        this.measurements_pv.push(Number(data2.pv_t13));
        this.measurements_pv.push(Number(data2.pv_t14));
        this.measurements_pv.push(Number(data2.pv_t15));
        this.measurements_pv.push(Number(data2.pv_t16));
        this.measurements_pv.push(Number(data2.pv_t17));
        this.measurements_pv.push(Number(data2.pv_t18));
        this.measurements_pv.push(Number(data2.pv_t19));
        this.measurements_pv.push(Number(data2.pv_t20));
        this.measurements_pv.push(Number(data2.pv_t21));
        this.measurements_pv.push(Number(data2.pv_t22));
        this.measurements_pv.push(Number(data2.pv_t23));
            
        this.measurements_genset = [];
        this.measurements_genset.push(Number(data2.genset_t00));
        this.measurements_genset.push(Number(data2.genset_t01));
        this.measurements_genset.push(Number(data2.genset_t02));
        this.measurements_genset.push(Number(data2.genset_t03));
        this.measurements_genset.push(Number(data2.genset_t04));
        this.measurements_genset.push(Number(data2.genset_t05));
        this.measurements_genset.push(Number(data2.genset_t06));
        this.measurements_genset.push(Number(data2.genset_t07));
        this.measurements_genset.push(Number(data2.genset_t08));
        this.measurements_genset.push(Number(data2.genset_t09));
        this.measurements_genset.push(Number(data2.genset_t10));
        this.measurements_genset.push(Number(data2.genset_t11));
        this.measurements_genset.push(Number(data2.genset_t12));
        this.measurements_genset.push(Number(data2.genset_t13));
        this.measurements_genset.push(Number(data2.genset_t14));
        this.measurements_genset.push(Number(data2.genset_t15));
        this.measurements_genset.push(Number(data2.genset_t16));
        this.measurements_genset.push(Number(data2.genset_t17));
        this.measurements_genset.push(Number(data2.genset_t18));
        this.measurements_genset.push(Number(data2.genset_t19));
        this.measurements_genset.push(Number(data2.genset_t20));
        this.measurements_genset.push(Number(data2.genset_t21));
        this.measurements_genset.push(Number(data2.genset_t22));
        this.measurements_genset.push(Number(data2.genset_t23));
        
        this.measurements_bess = [];
        this.measurements_bess.push(Number(data2.bess_t00));
        this.measurements_bess.push(Number(data2.bess_t01));
        this.measurements_bess.push(Number(data2.bess_t02));
        this.measurements_bess.push(Number(data2.bess_t03));
        this.measurements_bess.push(Number(data2.bess_t04));
        this.measurements_bess.push(Number(data2.bess_t05));
        this.measurements_bess.push(Number(data2.bess_t06));
        this.measurements_bess.push(Number(data2.bess_t07));
        this.measurements_bess.push(Number(data2.bess_t08));
        this.measurements_bess.push(Number(data2.bess_t09));
        this.measurements_bess.push(Number(data2.bess_t10));
        this.measurements_bess.push(Number(data2.bess_t11));
        this.measurements_bess.push(Number(data2.bess_t12));
        this.measurements_bess.push(Number(data2.bess_t13));
        this.measurements_bess.push(Number(data2.bess_t14));
        this.measurements_bess.push(Number(data2.bess_t15));
        this.measurements_bess.push(Number(data2.bess_t16));
        this.measurements_bess.push(Number(data2.bess_t17));
        this.measurements_bess.push(Number(data2.bess_t18));
        this.measurements_bess.push(Number(data2.bess_t19));
        this.measurements_bess.push(Number(data2.bess_t20));
        this.measurements_bess.push(Number(data2.bess_t21));
        this.measurements_bess.push(Number(data2.bess_t22));
        this.measurements_bess.push(Number(data2.bess_t23));

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
            name: 'PCC',
            data: this.measurements_pcc
          },{
            type: 'area',
            name: 'PV',
            data: this.measurements_pv
          },{
            type: 'area',
            name: 'BESS',
            data: this.measurements_bess
          },{
            type: 'area',
            name: 'GENSET',
            data: this.measurements_genset
          }
        ]
    
        this.updateFlag = true;
        if(this.measurements_pcc.length) {
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
        this.measurements_pcc = [];
        this.measurements_pcc.push(Number(data2.pcc_t00));
        this.measurements_pcc.push(Number(data2.pcc_t01));
        this.measurements_pcc.push(Number(data2.pcc_t02));
        this.measurements_pcc.push(Number(data2.pcc_t03));
        this.measurements_pcc.push(Number(data2.pcc_t04));
        this.measurements_pcc.push(Number(data2.pcc_t05));
        this.measurements_pcc.push(Number(data2.pcc_t06));
        this.measurements_pcc.push(Number(data2.pcc_t07));
        this.measurements_pcc.push(Number(data2.pcc_t08));
        this.measurements_pcc.push(Number(data2.pcc_t09));
        this.measurements_pcc.push(Number(data2.pcc_t10));
        this.measurements_pcc.push(Number(data2.pcc_t11));
        this.measurements_pcc.push(Number(data2.pcc_t12));
        this.measurements_pcc.push(Number(data2.pcc_t13));
        this.measurements_pcc.push(Number(data2.pcc_t14));
        this.measurements_pcc.push(Number(data2.pcc_t15));
        this.measurements_pcc.push(Number(data2.pcc_t16));
        this.measurements_pcc.push(Number(data2.pcc_t17));
        this.measurements_pcc.push(Number(data2.pcc_t18));
        this.measurements_pcc.push(Number(data2.pcc_t19));
        this.measurements_pcc.push(Number(data2.pcc_t20));
        this.measurements_pcc.push(Number(data2.pcc_t21));
        this.measurements_pcc.push(Number(data2.pcc_t22));
        this.measurements_pcc.push(Number(data2.pcc_t23));    
        
        this.measurements_pv = [];
        this.measurements_pv.push(Number(data2.pv_t00));
        this.measurements_pv.push(Number(data2.pv_t01));
        this.measurements_pv.push(Number(data2.pv_t02));
        this.measurements_pv.push(Number(data2.pv_t03));
        this.measurements_pv.push(Number(data2.pv_t04));
        this.measurements_pv.push(Number(data2.pv_t05));
        this.measurements_pv.push(Number(data2.pv_t06));
        this.measurements_pv.push(Number(data2.pv_t07));
        this.measurements_pv.push(Number(data2.pv_t08));
        this.measurements_pv.push(Number(data2.pv_t09));
        this.measurements_pv.push(Number(data2.pv_t10));
        this.measurements_pv.push(Number(data2.pv_t11));
        this.measurements_pv.push(Number(data2.pv_t12));
        this.measurements_pv.push(Number(data2.pv_t13));
        this.measurements_pv.push(Number(data2.pv_t14));
        this.measurements_pv.push(Number(data2.pv_t15));
        this.measurements_pv.push(Number(data2.pv_t16));
        this.measurements_pv.push(Number(data2.pv_t17));
        this.measurements_pv.push(Number(data2.pv_t18));
        this.measurements_pv.push(Number(data2.pv_t19));
        this.measurements_pv.push(Number(data2.pv_t20));
        this.measurements_pv.push(Number(data2.pv_t21));
        this.measurements_pv.push(Number(data2.pv_t22));
        this.measurements_pv.push(Number(data2.pv_t23));
            
        this.measurements_genset = [];
        this.measurements_genset.push(Number(data2.genset_t00));
        this.measurements_genset.push(Number(data2.genset_t01));
        this.measurements_genset.push(Number(data2.genset_t02));
        this.measurements_genset.push(Number(data2.genset_t03));
        this.measurements_genset.push(Number(data2.genset_t04));
        this.measurements_genset.push(Number(data2.genset_t05));
        this.measurements_genset.push(Number(data2.genset_t06));
        this.measurements_genset.push(Number(data2.genset_t07));
        this.measurements_genset.push(Number(data2.genset_t08));
        this.measurements_genset.push(Number(data2.genset_t09));
        this.measurements_genset.push(Number(data2.genset_t10));
        this.measurements_genset.push(Number(data2.genset_t11));
        this.measurements_genset.push(Number(data2.genset_t12));
        this.measurements_genset.push(Number(data2.genset_t13));
        this.measurements_genset.push(Number(data2.genset_t14));
        this.measurements_genset.push(Number(data2.genset_t15));
        this.measurements_genset.push(Number(data2.genset_t16));
        this.measurements_genset.push(Number(data2.genset_t17));
        this.measurements_genset.push(Number(data2.genset_t18));
        this.measurements_genset.push(Number(data2.genset_t19));
        this.measurements_genset.push(Number(data2.genset_t20));
        this.measurements_genset.push(Number(data2.genset_t21));
        this.measurements_genset.push(Number(data2.genset_t22));
        this.measurements_genset.push(Number(data2.genset_t23));
        
        this.measurements_bess = [];
        this.measurements_bess.push(Number(data2.bess_t00));
        this.measurements_bess.push(Number(data2.bess_t01));
        this.measurements_bess.push(Number(data2.bess_t02));
        this.measurements_bess.push(Number(data2.bess_t03));
        this.measurements_bess.push(Number(data2.bess_t04));
        this.measurements_bess.push(Number(data2.bess_t05));
        this.measurements_bess.push(Number(data2.bess_t06));
        this.measurements_bess.push(Number(data2.bess_t07));
        this.measurements_bess.push(Number(data2.bess_t08));
        this.measurements_bess.push(Number(data2.bess_t09));
        this.measurements_bess.push(Number(data2.bess_t10));
        this.measurements_bess.push(Number(data2.bess_t11));
        this.measurements_bess.push(Number(data2.bess_t12));
        this.measurements_bess.push(Number(data2.bess_t13));
        this.measurements_bess.push(Number(data2.bess_t14));
        this.measurements_bess.push(Number(data2.bess_t15));
        this.measurements_bess.push(Number(data2.bess_t16));
        this.measurements_bess.push(Number(data2.bess_t17));
        this.measurements_bess.push(Number(data2.bess_t18));
        this.measurements_bess.push(Number(data2.bess_t19));
        this.measurements_bess.push(Number(data2.bess_t20));
        this.measurements_bess.push(Number(data2.bess_t21));
        this.measurements_bess.push(Number(data2.bess_t22));
        this.measurements_bess.push(Number(data2.bess_t23));

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
            name: 'PCC',
            data: this.measurements_pcc
          },{
            type: 'area',
            name: 'PV',
            data: this.measurements_pv
          },{
            type: 'area',
            name: 'BESS',
            data: this.measurements_bess
          },{
            type: 'area',
            name: 'GENSET',
            data: this.measurements_genset
          }
        ]
        
        this.now2 = new Date()
        this.chartOptions.plotOptions.series.pointStart = this.now2.setHours(this.now2.getHours()-this.SP_Timezone-23)   

        this.updateFlag = true;
        if(this.measurements_pcc.length) {
          this.updateData = true;
        }
    });
  }
}