import React from 'react';
import {storiesOf} from '@storybook/react';
// import {action} from '@storybook/addon-actions';
import {withInfo} from '@storybook/addon-info';

import StackedBarChart from 'app/components/stackedBarChart';

storiesOf('StackedBarChart', module).add(
  'default',
  withInfo('')(() => (
    <div style={{height: 400}}>
      <StackedBarChart
        series={[
          {
            data: [{x: 1461099600, y: 31734}, {x: 1461103200, y: 36790}],
            label: 'received',
          },
          {
            data: [{x: 1461099600, y: 2867}, {x: 1461103200, y: 2742}],
            label: 'rejected',
          },
          {
            data: [{x: 1461099600, y: 0}, {x: 1461103200, y: 0}],
            label: 'blacklisted',
          },
        ]}
        className="standard-barchart"
        height="100%"
        label="events"
        barClasses={['received', 'blacklisted', 'rejected']}
      />
    </div>
  ))
);
