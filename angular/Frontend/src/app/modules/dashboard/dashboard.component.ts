import { Component, OnInit } from '@angular/core';
import { Measurements_24hours } from 'src/app/shared/model/measurements_24hours.model';
import { Milp_parameters } from 'src/app/shared/model/milp_parameter.model';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  private intervalUpdate: any = null;

  public measurements_pcc = new Array();
  public measurements_pv = new Array();
  public measurements_genset = new Array();
  public measurements_bess = new Array();
  public measurements_bess_soc = new Array();
  public costsChart = new Array();
  public total_daily_generation: number;
  public total_daily_consumption: number;
  public total_daily_cost: number;
  public now2 = new Date();
  public SP_Timezone = 3


  constructor(private http: HttpClient) {
    this.showData()
  }

  ngOnInit(): void {
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

        this.total_daily_generation = 0.0;
        this.total_daily_consumption = 0.0;

        for (let i = 0; i < this.measurements_pv.length; i++) {
          this.total_daily_generation = this.total_daily_generation + Math.abs(this.measurements_pv[i]);
        }
        for (let i = 0; i < this.measurements_genset.length; i++) {
          this.total_daily_generation = this.total_daily_generation + Math.abs(this.measurements_genset[i]);
        }
        for (let i = 0; i < this.measurements_bess.length; i++) {
          if (this.measurements_bess[i] > 0.0) {
            this.total_daily_generation = this.total_daily_generation + Math.abs(this.measurements_bess[i]);
          }
        }
        for (let i = 0; i < this.measurements_pcc.length; i++) {
          this.total_daily_consumption = this.total_daily_consumption + this.measurements_pcc[i];
        }

        this.total_daily_generation = Math.round(100 * this.total_daily_generation)/100;
        this.total_daily_consumption = Math.round(100 * this.total_daily_consumption)/100;

        this.http.get<Milp_parameters>('http://localhost:8051/v1/api/milp_parameters/1/')
        .subscribe(
          data2 => {
            this.costsChart = [];
            this.costsChart.push(Number(data2.pcc_cost_t24));
            this.costsChart.push(Number(data2.pcc_cost_t01));
            this.costsChart.push(Number(data2.pcc_cost_t02));
            this.costsChart.push(Number(data2.pcc_cost_t03));
            this.costsChart.push(Number(data2.pcc_cost_t04));
            this.costsChart.push(Number(data2.pcc_cost_t05));
            this.costsChart.push(Number(data2.pcc_cost_t06));
            this.costsChart.push(Number(data2.pcc_cost_t07));
            this.costsChart.push(Number(data2.pcc_cost_t08));
            this.costsChart.push(Number(data2.pcc_cost_t09));
            this.costsChart.push(Number(data2.pcc_cost_t10));
            this.costsChart.push(Number(data2.pcc_cost_t11));
            this.costsChart.push(Number(data2.pcc_cost_t12));
            this.costsChart.push(Number(data2.pcc_cost_t13));
            this.costsChart.push(Number(data2.pcc_cost_t14));
            this.costsChart.push(Number(data2.pcc_cost_t15));
            this.costsChart.push(Number(data2.pcc_cost_t16));
            this.costsChart.push(Number(data2.pcc_cost_t17));
            this.costsChart.push(Number(data2.pcc_cost_t18));
            this.costsChart.push(Number(data2.pcc_cost_t19));
            this.costsChart.push(Number(data2.pcc_cost_t20));
            this.costsChart.push(Number(data2.pcc_cost_t21));
            this.costsChart.push(Number(data2.pcc_cost_t22));
            this.costsChart.push(Number(data2.pcc_cost_t23));

            // this.now2.setHours(this.now2.getHours()-this.SP_Timezone-23)
            // let hour = this.now2.getHours() - this.SP_Timezone
            let hour = this.now2.getHours()
            // console.log("********* Time ********")
            // console.log(hour)
            // console.log(this.costsChart)
            // console.log(this.measurements_pcc)
            
            this.total_daily_cost = 0.0;
            // console.log("********* Loop 1 ********")
            for (let i = hour + 1; i < this.costsChart.length; i++) {
              this.total_daily_cost = this.total_daily_cost + this.measurements_pcc[i - hour - 1] * this.costsChart[i];
              // console.log(i)
              // console.log(this.costsChart[i])
              // console.log(this.measurements_pcc[i - hour - 1])
            }
            // console.log("********* Loop 2 ********")
            for (let i = 0; i < hour + 1; i++) {
              this.total_daily_cost = this.total_daily_cost + this.measurements_pcc[i + (23 - hour)] * this.costsChart[i];
              // console.log(i)
              // console.log(this.costsChart[i])
              // console.log(this.measurements_pcc[i + (23 - hour)])
            }
            // this.total_daily_cost = Math.round(100 * this.total_daily_cost)/100;
    
      });

    });
  }
}
