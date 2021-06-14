<template>
  <FancyList
    :items="items"
    :show-controls="showControls"
    :filter-definitions="filterDefinitions"
    :context="context"
    :searchable-fields="searchableFields"
    :num-items-options="numItemsOptions"
    :sort-definitions="sortDefinitions"
    :default-items-per-page="defaultItemsPerPage"
    :loaded="loaded"
>
    <template #loading>
      Experimenten worden geladen
    </template>

    <template #no_items>
      Er zijn op dit moment geen experimenten waarvoor je je kunt opgeven.
    </template>

    <template #title="{ item: experiment, context }">
      <h5 v-html="experiment.name">
      </h5>
    </template>

    <template #undertitle="{ item: experiment, context }">
      <div class="ufl-undertitle-line">
        Type: {{ experiment.use_timeslots ? "op locatie" : "online" }}
      </div>
      <div class="ufl-undertitle-line">
        Compensatie: {{ experiment.compensation }}
      </div>
      <div class="ufl-undertitle-line">
        Duur: {{ experiment.duration }}
      </div>
      <div class="ufl-undertitle-line">
        <a :href="$url('participant:register', [experiment.id])" class="register-link">Inschrijven</a>
      </div>
    </template>

    <template #details="{ item: experiment, context }">
      <div class="row">
        <div class="col-12">
          <p>
            Dit experiment duurt {{ experiment.duration }}.
            <span v-if="experiment.location">
              Het wordt afgenomen op
              <a
                  v-if="experiment.location.route_url"
                  :href="experiment.location.route_url"
                  target="_blank"
              >
                {{ experiment.location.name }}
              </a>
              <span v-else>
                {{ experiment.location.name }}
              </span>
            </span>
          </p>
          <p>
            Bijzonderheden
            <ul>
              <li>
                Je krijgt {{ experiment.compensation }} om mee te doen.
              </li>
              <li v-if="experiment.task_description">
                {{ experiment.task_description }}
              </li>
              <li v-if="experiment.additional_instructions">
                {{ experiment.additional_instructions }}
              </li>
            </ul>
          </p>
          <button class="button-colored register-button" @click="window.open($url('participant:register', [experiment.id]))">
            Inschrijven
          </button>
        </div>
      </div>
    </template>

  </FancyList>
</template>
<script>

import FancyList from "../../../../django-shared-core/uil/vue/static/vue/components/fancy-list/FancyList";

export default {
  name: 'ExperimentList',
  components: {
    FancyList
  },
  data() {
    return {
      // Actual data loaded through $ufl_load in mounted()
      'items': [],
      'showControls': false,
      'context': {},
      'searchableFields': [],
      'filterDefinitions': {},
      'numItemsOptions': [],
      'sortDefinitions': {},
      'defaultItemsPerPage': 99999,
      'loaded': false,
    };
  },
  mounted() {
    this.$ufl_load(this, this.$url('main:home_api', []));
  },
}
</script>

<style>
.leader-image {
    max-height: 200px;
    max-width: 400px;
}
.register-link {
  margin-left: 5px;
}
.register-button {
  position: absolute;
  bottom: 0;
  right: 15px;
}

@media (max-width: 767px) {
    .register-link {
      margin-left: 0;
    }
    .register-button {
      display: block;
      position: initial;
      margin: 0 auto;
    }
}
</style>