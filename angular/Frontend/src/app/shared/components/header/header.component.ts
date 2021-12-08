import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { MODES, sharedState } from '../../model/sharedState.model';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  @Output() toggleSideBarForMe: EventEmitter<any> = new EventEmitter();
  
  constructor(private state: sharedState) { }

  ngOnInit(): void {
  }

  toggleSideBar() {
    this.toggleSideBarForMe.emit();
    setTimeout(() => {
      window.dispatchEvent(
        new Event('Resize')
      );
    }, 300)
  }

  stopState() {
    this.state.mode = MODES.STOP;
  }

  playState() {
    this.state.mode = MODES.PLAY;
  }


}
