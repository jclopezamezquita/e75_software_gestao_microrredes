import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
// import { Chart } from 'chart.js';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { MODES, sharedState } from '../../model/sharedState.model';

@Component({
  selector: 'app-widget-realtime',
  templateUrl: './realtime.component.html',
  styleUrls: ['./realtime.component.scss']
})
export class RealtimeComponent {

  /*
  * Interval to update the chart
  * @var {any} intervalUpdate
  */
  private intervalUpdate: any = null;

  /*
   * The ChartJS Object
   * @var {any} chart
   */
  public chart: any = null;

  constructor(private http: HttpClient, private share: sharedState) { }

  /*
  * On component initialization
  * @function ngOnInit
  * @return {void}
  */
  private ngOnInit(): void {

    this.chart = new Chart('realtime', {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Data',
            fill: false,
            data: [],
            backgroundColor: '#168ede',
            borderColor: '#168ede'
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            enabled: true
          },
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              color: 'white'
            }
          }
        },
        scales: {
          y: {
            ticks: {
              color: 'white'
            }
          },
          x: {
            ticks: {
              color: 'white'
            },
            beginAtZero: true
          }
        }
      }
    });

    this.intervalUpdate = setInterval(function(){
      if(this.share.mode == MODES.PLAY) {
        this.showData();
      }
    }.bind(this), 500);
  }

  /*
  * On component destroy
  * @function ngOnDestroy
  * @return {void}
  */
  private ngOnDestroy(): void {
    clearInterval(this.intervalUpdate);
  }

  /*
   * Print the data to the chart
   * @function showData
   * @return {void}
   */
  private showData(): void {
    this.getFromAPI().subscribe(response => {
      if(response.error === false) {
        let chartTime: any = new Date();
        chartTime = chartTime.getHours() + ':' + ((chartTime.getMinutes() < 10) ? '0' + chartTime.getMinutes() : chartTime.getMinutes()) + ':' + ((chartTime.getSeconds() < 10) ? '0' + chartTime.getSeconds() : chartTime.getSeconds());
				if(this.chart.data.labels.length > 15) {
          this.chart.data.labels.shift();
          this.chart.data.datasets[0].data.shift();
        }
        this.chart.data.labels.push(chartTime);
        this.chart.data.datasets[0].data.push(response.data);
        this.chart.update();
       } else {
        console.error("ERROR: The response had an error, retrying");
       }
    }, error => {
     console.error("ERROR: Unexpected response");
    });
  }
  
  /*
  * Get the data from the API
  * @function getFromAPI
  * @return {Observable<any>}
  */
  private getFromAPI(): Observable<any>{
    return this.http.get(
      'http://localhost:8051/random',
      { responseType: 'json' }
    );
  }
}
