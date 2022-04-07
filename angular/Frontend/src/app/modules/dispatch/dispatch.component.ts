import { Component, OnInit } from '@angular/core';
import { Economic_dispatch } from 'src/app/shared/model/economic_dispatch.model';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-dispatch',
  templateUrl: './dispatch.component.html',
  styleUrls: ['./dispatch.component.scss']
})
export class DispatchComponent implements OnInit {

  public dispatchData_BESS = new Array();
  public dispatchData_load = new Array();
  public dispatchData_PV = new Array();
  public dispatchData_genset = new Array();

  constructor(private http: HttpClient) {

    this.http.get<Economic_dispatch>('http://192.168.192.47:8051/v1/api/economic_dispatch/1/')
      .subscribe(
        data2 => {
          this.dispatchData_BESS = [];
          this.dispatchData_BESS.push(Number(data2.bat_power_t00));
          this.dispatchData_BESS.push(Number(data2.bat_power_t01));
          this.dispatchData_BESS.push(Number(data2.bat_power_t02));
          this.dispatchData_BESS.push(Number(data2.bat_power_t03));
          this.dispatchData_BESS.push(Number(data2.bat_power_t04));
          this.dispatchData_BESS.push(Number(data2.bat_power_t05));
          this.dispatchData_BESS.push(Number(data2.bat_power_t06));
          this.dispatchData_BESS.push(Number(data2.bat_power_t07));
          this.dispatchData_BESS.push(Number(data2.bat_power_t08));
          this.dispatchData_BESS.push(Number(data2.bat_power_t09));
          this.dispatchData_BESS.push(Number(data2.bat_power_t10));
          this.dispatchData_BESS.push(Number(data2.bat_power_t11));
          this.dispatchData_BESS.push(Number(data2.bat_power_t12));
          this.dispatchData_BESS.push(Number(data2.bat_power_t13));
          this.dispatchData_BESS.push(Number(data2.bat_power_t14));
          this.dispatchData_BESS.push(Number(data2.bat_power_t15));
          this.dispatchData_BESS.push(Number(data2.bat_power_t16));
          this.dispatchData_BESS.push(Number(data2.bat_power_t17));
          this.dispatchData_BESS.push(Number(data2.bat_power_t18));
          this.dispatchData_BESS.push(Number(data2.bat_power_t19));
          this.dispatchData_BESS.push(Number(data2.bat_power_t20));
          this.dispatchData_BESS.push(Number(data2.bat_power_t21));
          this.dispatchData_BESS.push(Number(data2.bat_power_t22));
          this.dispatchData_BESS.push(Number(data2.bat_power_t23));
          // console.log("this.dispatchData_BESS: ");
          // console.log(this.dispatchData_BESS);
    
          this.dispatchData_load = [];
          this.dispatchData_load.push(Number(data2.load_curt_t00));
          this.dispatchData_load.push(Number(data2.load_curt_t01));
          this.dispatchData_load.push(Number(data2.load_curt_t02));
          this.dispatchData_load.push(Number(data2.load_curt_t03));
          this.dispatchData_load.push(Number(data2.load_curt_t04));
          this.dispatchData_load.push(Number(data2.load_curt_t05));
          this.dispatchData_load.push(Number(data2.load_curt_t06));
          this.dispatchData_load.push(Number(data2.load_curt_t07));
          this.dispatchData_load.push(Number(data2.load_curt_t08));
          this.dispatchData_load.push(Number(data2.load_curt_t09));
          this.dispatchData_load.push(Number(data2.load_curt_t10));
          this.dispatchData_load.push(Number(data2.load_curt_t11));
          this.dispatchData_load.push(Number(data2.load_curt_t12));
          this.dispatchData_load.push(Number(data2.load_curt_t13));
          this.dispatchData_load.push(Number(data2.load_curt_t14));
          this.dispatchData_load.push(Number(data2.load_curt_t15));
          this.dispatchData_load.push(Number(data2.load_curt_t16));
          this.dispatchData_load.push(Number(data2.load_curt_t17));
          this.dispatchData_load.push(Number(data2.load_curt_t18));
          this.dispatchData_load.push(Number(data2.load_curt_t19));
          this.dispatchData_load.push(Number(data2.load_curt_t20));
          this.dispatchData_load.push(Number(data2.load_curt_t21));
          this.dispatchData_load.push(Number(data2.load_curt_t22));
          this.dispatchData_load.push(Number(data2.load_curt_t23));
          // console.log("this.dispatchData_load: ");
          // console.log(this.dispatchData_load);
    
          this.dispatchData_PV = [];
          this.dispatchData_PV.push(Number(data2.pv_curt_t00));
          this.dispatchData_PV.push(Number(data2.pv_curt_t01));
          this.dispatchData_PV.push(Number(data2.pv_curt_t02));
          this.dispatchData_PV.push(Number(data2.pv_curt_t03));
          this.dispatchData_PV.push(Number(data2.pv_curt_t04));
          this.dispatchData_PV.push(Number(data2.pv_curt_t05));
          this.dispatchData_PV.push(Number(data2.pv_curt_t06));
          this.dispatchData_PV.push(Number(data2.pv_curt_t07));
          this.dispatchData_PV.push(Number(data2.pv_curt_t08));
          this.dispatchData_PV.push(Number(data2.pv_curt_t09));
          this.dispatchData_PV.push(Number(data2.pv_curt_t10));
          this.dispatchData_PV.push(Number(data2.pv_curt_t11));
          this.dispatchData_PV.push(Number(data2.pv_curt_t12));
          this.dispatchData_PV.push(Number(data2.pv_curt_t13));
          this.dispatchData_PV.push(Number(data2.pv_curt_t14));
          this.dispatchData_PV.push(Number(data2.pv_curt_t15));
          this.dispatchData_PV.push(Number(data2.pv_curt_t16));
          this.dispatchData_PV.push(Number(data2.pv_curt_t17));
          this.dispatchData_PV.push(Number(data2.pv_curt_t18));
          this.dispatchData_PV.push(Number(data2.pv_curt_t19));
          this.dispatchData_PV.push(Number(data2.pv_curt_t20));
          this.dispatchData_PV.push(Number(data2.pv_curt_t21));
          this.dispatchData_PV.push(Number(data2.pv_curt_t22));
          this.dispatchData_PV.push(Number(data2.pv_curt_t23));
          // console.log("this.dispatchData_PV: ");
          // console.log(this.dispatchData_PV);

          this.dispatchData_genset = [];
          this.dispatchData_genset.push(Number(data2.genset_power_t00));
          this.dispatchData_genset.push(Number(data2.genset_power_t01));
          this.dispatchData_genset.push(Number(data2.genset_power_t02));
          this.dispatchData_genset.push(Number(data2.genset_power_t03));
          this.dispatchData_genset.push(Number(data2.genset_power_t04));
          this.dispatchData_genset.push(Number(data2.genset_power_t05));
          this.dispatchData_genset.push(Number(data2.genset_power_t06));
          this.dispatchData_genset.push(Number(data2.genset_power_t07));
          this.dispatchData_genset.push(Number(data2.genset_power_t08));
          this.dispatchData_genset.push(Number(data2.genset_power_t09));
          this.dispatchData_genset.push(Number(data2.genset_power_t10));
          this.dispatchData_genset.push(Number(data2.genset_power_t11));
          this.dispatchData_genset.push(Number(data2.genset_power_t12));
          this.dispatchData_genset.push(Number(data2.genset_power_t13));
          this.dispatchData_genset.push(Number(data2.genset_power_t14));
          this.dispatchData_genset.push(Number(data2.genset_power_t15));
          this.dispatchData_genset.push(Number(data2.genset_power_t16));
          this.dispatchData_genset.push(Number(data2.genset_power_t17));
          this.dispatchData_genset.push(Number(data2.genset_power_t18));
          this.dispatchData_genset.push(Number(data2.genset_power_t19));
          this.dispatchData_genset.push(Number(data2.genset_power_t20));
          this.dispatchData_genset.push(Number(data2.genset_power_t21));
          this.dispatchData_genset.push(Number(data2.genset_power_t22));
          this.dispatchData_genset.push(Number(data2.genset_power_t23));

    });

  }

  ngOnInit(): void {
  }

}
