import React from 'react';
import {Composition} from 'remotion';
import {Trick} from './Trick';
import {Formeln} from './Formeln';
import {FormelVergleich} from './FormelVergleich';
import Z from './zeiten.json';

export const RemotionRoot = () => (<>
  <Composition id="Trick" component={Trick} durationInFrames={Math.round(Z.laenge * 30)}
    fps={30} width={1280} height={720} />
  <Composition id="Formeln" component={Formeln} durationInFrames={30} fps={30} width={1280} height={720} />
  <Composition id="FormelVergleich" component={FormelVergleich} durationInFrames={30} fps={30} width={1280} height={720} />
</>);
