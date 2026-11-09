import React from 'react';
import {Composition, Still} from 'remotion';
import {Video, gesamtFrames} from './Video';
import {Titelkarte, ThumbnailA, ThumbnailB, ThumbnailC} from './Titel';

export const RemotionRoot = () => (<>
  <Composition id="Erklaervideo" component={Video} durationInFrames={gesamtFrames} fps={30} width={1920} height={1080} />
  <Still id="Titelbild" component={Titelkarte} defaultProps={{animiert: false}} width={1920} height={1080} />
  <Still id="ThumbnailA" component={ThumbnailA} width={1920} height={1080} />
  <Still id="ThumbnailB" component={ThumbnailB} width={1920} height={1080} />
  <Still id="ThumbnailC" component={ThumbnailC} width={1920} height={1080} />
</>);
